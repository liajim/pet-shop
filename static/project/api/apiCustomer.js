function getUrlAddCustomer() {
    return `/api/customers/`;
}

function addCustomer(props, callback, onErrorCb){
    genericPost(getUrlAddCustomer(), props, callback, onErrorCb);
}
