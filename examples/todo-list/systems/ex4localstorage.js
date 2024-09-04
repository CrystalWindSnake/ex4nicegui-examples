function ex4ng_loadDataFromLocalStorage(key) {
    const jsonString = localStorage.getItem(key);

    if (jsonString) {
        const value = JSON.parse(jsonString);
        return value;
    } else {
        return null;
    }
}


function ex4ng_saveToLocalStorage(key, data) {
    const jsonString = JSON.stringify(data);
    localStorage.setItem(key, jsonString);
}