/**
 * This script formats a JSON following the array key order and object keys from a previous one.
 * This is useful for updating a JSON file while reducing the number of lines changed (ignoring whitespace).
 * 
 * Inputs: It requires 2 JSON files as inputs at the same level of the script file.
 * - new.json: JSON (Object) to be formatted.
 * - old.json: JSON (Object) to take as a reference to sort and format.
 * Output:
 * - generated.json: JSON that contains the new.json data using the old.json key order
 */

const fs = require('fs');


const JSON_STRUCTURE = [{
    arr: 'products',
    key: 'sku',
    items: [{
        arr: 'specialTerms',
        key: 'name',
    }]
}];

const oldJson = readJson('old.json');
const newJson = readJson('new.json');

const orderedJson = generateSortedJSON(newJson, oldJson, JSON_STRUCTURE);
const orderedJsonString = JSON.stringify(orderedJson, null, 2); 

fs.writeFile('generated.json', orderedJsonString, err => {
    if (err) {
      console.error(err)
      return
    }
});



function readJson(path) {
    const json = fs.readFileSync(path);
    return JSON.parse(json)
}

function generateOrderedKeys(actualKeys, oldKeys) {
    // return sorted actualKeys using oldKeys order
    const commonKeys = oldKeys.filter(x => actualKeys.includes(x));
    const newKeys = actualKeys.filter(x => !oldKeys.includes(x) );

    const orderedKeys = [...commonKeys, ...newKeys];
    return orderedKeys;
}

function generateSortedObjectByKeys(obj, orderedKeys) {
    // generated ordered object by keys (2nd parameter)
    const rv = {};
    for (const key of orderedKeys)
      rv[key] = obj[key];
    return rv;
}

function generateSortedArrayByElement(arr, idKeyField, orderedIdKeys) {
    // return sorted array using orderedIdKeys order
    const map = new Map();
    for (const obj of arr)
        map.set(obj[idKeyField], obj);
    
    const orderedArr = orderedIdKeys.map(k => map.get(k));
    return orderedArr;
}


function generateSortedJSON(newJson, oldJson, orderStructure) {
    // return sorted Json object
    // parent level
    const orderedKeys = generateOrderedKeys(Object.keys(newJson), Object.keys(oldJson));
    const parent = generateSortedObjectByKeys(newJson, orderedKeys);
    generateSortedArray(parent, oldJson, orderStructure);
    return parent;
}


function generateSortedArray(newParent, oldParent, levelKeys) {
    if (!oldParent)
        return;
    for (const lvlItem of levelKeys) {
        const newArr = newParent[lvlItem.arr];
        const oldArr = oldParent[lvlItem.arr];
        if (!newArr || !oldArr)
            continue;
        const sortedArr = generateSortedArrayByKey(newArr, oldArr, lvlItem.key);
        newParent[lvlItem.arr] = sortedArr;
        if (lvlItem.items) {
            for (const elm of sortedArr) {
                const newParent = elm;
                const oldParent = oldArr.find(x => x[lvlItem.key] == elm[lvlItem.key]);
                generateSortedArray(newParent, oldParent, lvlItem.items);
            }
        }
    }
}

function generateSortedArrayByKey(newArr, oldArr, idKeyField) {
    if (newArr.length === 0 || oldArr.length === 0) {
        return newArr;
    }

    const newArrKeys = newArr.map(x=> x[idKeyField]);
    const oldArrKeys = oldArr.map(x=> x[idKeyField]);
    const sortedArrKeys = generateOrderedKeys(newArrKeys, oldArrKeys);

    const newObjKeys = Object.keys(newArr[0]);
    const oldObjKeys = Object.keys(oldArr[0]);
    const sortedObjKeys = generateOrderedKeys(newObjKeys, oldObjKeys);

    const orderedArrKeys = generateSortedArrayByElement(newArr, idKeyField, sortedArrKeys);
    return orderedArrKeys.map(x => generateSortedObjectByKeys(x, sortedObjKeys));
}
