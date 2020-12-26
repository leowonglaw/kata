import re
import argparse
import subprocess, os, platform, shutil
import xml.etree.ElementTree as ET


parser = argparse.ArgumentParser(description="Repairs atlassian-maven's build")
parser.add_argument('input', action='store', nargs="?",
    choices=['cache', 'lombok'],
    default='cache', const='cache',
    help='repair mode (default: %(default)s)')

POM_FILENAME = "pom.xml"
SOURCE_DIR = "src"


def handle_error(function):
    def wrap_function(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except:
            if not kwargs.get('ignore_errors'):
                raise
    return wrap_function


class CommandExecuter:

    def __init__(self):
        self.startupinfo = None
        if platform == 'win32':
            self.startupinfo = subprocess.STARTUPINFO()
            self.startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

    @handle_error
    def execute(self, command, silently=False, **kwargs):
        if silently:
            return self._execute_in_background(command)
        else:
            return self._execute_in_foreground(command)

    def _execute_in_foreground(self, command):
        os.system(command)

    def _execute_in_background(self, command):
        command_arguments = command.split(" ")
        result  = subprocess.run(command_arguments, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.stderr:
            raise Exception(result.stderr)
        return result.stdout.decode()


class AtlasMavenAPI:

    def __init__(self, command_executer):
        self.command_executer = command_executer

    def clean(self, **kwargs):
        self._execute_command("atlas-clean", **kwargs)

    def package(self, **kwargs):
        self._execute_command("atlas-package", **kwargs)

    def list_packages(self, **kwargs):
        self._execute_command("atlas-mvn dependency:build-classpath -e -DincludeArtifactIds=lombok", **kwargs)

    def _execute_command(self, *args, **kwargs):
        return self.command_executer.execute(*args, **kwargs)


class LombokApi:

    ARTIFACT = 'lombok'
    JAR_PATH_REGEX = re.compile(r'^[^ []\S*$', re.MULTILINE)

    def __init__(self, command_executer):
        self.command_executer = command_executer

    def delombok(self, destiny, source="src"):
        cmd = f"java -jar {self.jar_path} delombok {source} -d {destiny}"
        self._execute_command(cmd, silently=True, ignore_errors=True)

    @property
    def jar_path(self):
        cmd = f"atlas-mvn dependency:build-classpath -e -DincludeArtifactIds={self.ARTIFACT}"
        stout = self._execute_command(cmd, silently=True)
        return self.JAR_PATH_REGEX.search(stout).group()

    def _execute_command(self, *args, **kwargs):
        return self.command_executer.execute(*args, **kwargs)


class LombokFixer:

    def __init__(self, lombok_service, mvn_service):
        self.lombok_service = lombok_service
        self.mvn_service = mvn_service

    class RepairManager:

        def __init__(self, backup_path="src_bak"):
            self.backup_path = backup_path

        def __enter__(self):
            os.rename(SOURCE_DIR, self.backup_path)
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            shutil.rmtree(SOURCE_DIR)
            os.rename(self.backup_path, SOURCE_DIR)

    def repair(self):
        backup_path = "src_bak"
        self.mvn_service.clean(silently=True)
        with self.RepairManager(backup_path):
            self.lombok_service.delombok(
                source=backup_path,
                destiny=SOURCE_DIR
            )
            self.mvn_service.package()


class AtlasMavenByPass:

    MAVEN_SETTINGS = {
        '': "http://maven.apache.org/POM/4.0.0",
        'xsi': "http://www.w3.org/2001/XMLSchema-instance",
    }
    XML_NAMESPACE = {
        'maven': MAVEN_SETTINGS.get('')
    }

    class RepairManager:

        def __init__(self, backup_path="pom.xml.bak"):
            self.backup_path = backup_path

        def __enter__(self):
            shutil.copy2(POM_FILENAME, self.backup_path)
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            os.remove(POM_FILENAME)
            os.rename(self.backup_path, POM_FILENAME)

    def __init__(self, maven_service):
        self.maven_service = maven_service
        for key, value in self.MAVEN_SETTINGS.items():
            ET.register_namespace(key, value)

    def repair(self):
        with self.RepairManager():
            self.maven_service.clean(silently=True)
            self._create_uncached_pom(output_path=POM_FILENAME)
            self.maven_service.package(silently=True, ignore_errors=True)
            self.maven_service.package()

    def _create_uncached_pom(self, output_path):
        pom_tree = ET.parse(POM_FILENAME)
        pom_root = pom_tree.getroot()
        self.__swap_last_dependencies(pom_root)
        pom_tree.write(output_path)

    def __swap_last_dependencies(self, pom_root):
        dependencies_tag = self._get_dependencies_tag(pom_root)
        dependencies_elements = list(dependencies_tag.getchildren())
        second_last_dependency = dependencies_elements[-2]
        dependencies_tag.remove(second_last_dependency)
        dependencies_tag.append(second_last_dependency)

    def _get_dependencies_tag(self, pom_root):
        dependencies_tag = pom_root.find('maven:dependencies', self.XML_NAMESPACE)
        if dependencies_tag is None:
            raise ValueError("Maven dependencies not found. Be sure that your maven version is 4.0.0.")
        return dependencies_tag


class RepairFactory:

    def __init__(self):
        self.executer = CommandExecuter()
        self.atlas_mvn = AtlasMavenAPI(self.executer)

    def build_fixer(self, opt):
        if args.input == 'cache':
            return AtlasMavenByPass(self.atlas_mvn)
        else:
            lombok_api = LombokApi(self.executer)
            return LombokFixer(lombok_api, self.atlas_mvn)


if __name__ == "__main__":
    args = parser.parse_args()
    factory = RepairFactory()
    fixer = factory.build_fixer(args.input)
    fixer.repair()
