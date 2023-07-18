$(function () {

    // Start counting from the third row
    var counter = 1;

    $("#insertRow").on("click", function (event) {
        event.preventDefault();

        var newRow = $("<tr>");
        var cols = '';
        // Table columns
        cols += '<th scrope="row">' + counter + '</th>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="product_variants"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="product"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="description"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="length"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="width"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="quantity"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="uom"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="page_number"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="position"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="unit_price"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="taxes"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name="disc"></td>';
        cols += '<td><input class="form-control rounded-0 txt_custom" type="text" name=""></td>';
        cols += '<td><button class="btn btn-danger_new rounded-0" id ="deleteRow"><i class="fa fa-trash"></i></button</td>';

        // Insert the columns inside a row
        newRow.append(cols);

        // Insert the row inside a table
        $("table").append(newRow);

        // Increase counter after each row insertion
        counter++;
    });

    // Remove row when delete btn is clicked
    $("table").on("click", "#deleteRow", function (event) {
        $(this).closest("tr").remove();
        counter -= 1
    });
});





