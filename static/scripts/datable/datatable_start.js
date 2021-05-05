$(document).ready(function () {
    $('#example').DataTable({
        select: true,
        dom: 'Bfrtip',
        buttons: [
            'pdf', 'print'
        ]
    });
});