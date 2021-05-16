function getUrlUpdateCustomer(id) {
    return `/api/internal/customers/${id}/`;
}

function updateCustomer(props, callback, onErrorCb){
    genericPatch(getUrlUpdateCustomer(props.id), props.data, callback, onErrorCb);
}
