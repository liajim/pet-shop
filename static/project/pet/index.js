$(document).ready(function() {
    function heartUnheartPet(e, class_to_remove, class_to_add) {
        var i = parseInt($(e.target).attr('id'));
        var data_to_send = { id: customer_id, data: {pet_id: i}}
        updateCustomer(data_to_send,
            (data) => {
                $(e.target).removeClass(class_to_remove);
                $(e.target).addClass(class_to_add);
            },
            (xhr, status, error) => {
                swal("Error", xhr.responseText.substring(0, 400), "error");
                console.log(xhr, error);
            }
        );
    }
    var columns = [
            {
                data: "photo_url",
                orderable: false,
                render: function(data) {
                        return '<img height="100px" src="'+data+'"/>'
                        }
            },
            { data: "name", orderable: true },
            { data: "specie", orderable: true },
            { data: "breed", orderable: true },
            { data: "sex", orderable: true },
            { data: "age", orderable: true },
            {
                data: "price",
                orderable: true,
                render: function(data, type, row) {
                            if (data)
                                return data;
                            else
                                return "For Adoption";
                        }
            },
        ];
    if (has_customer) {
        columns.push({
            data: "is_hearted",
                orderable: true,
                render: function(data, type, row) {
                            if (data)
                                return '<i class="icon-heart icon-5x icon-red" title="Unheart this pet" id="' + row.id + '"></i>';
                            else
                                return '<i class="icon-heart-empty icon-5x icon-gray" title="Heart this pet" id="' + row.id + '"></i>';
                        }
        })
    }
    var table = $('#petTable').DataTable( {
        processing: true,
        serverSide: true,
        'ajax': '/api/pets/',
        columns: columns
    }).on( 'draw.dt', function () {
        var heart_classes = ['icon-heart', 'icon-red'];
        var un_heart_classes = ['icon-heart-empty', 'icon-gray'];
        $('.icon-heart').click((e)=>{
            heartUnheartPet(e, heart_classes, un_heart_classes);
        })
        $('.icon-heart-empty').click((e)=>{
            heartUnheartPet(e, un_heart_classes, heart_classes);
        })
    });

});