// These formulas are only available to use for GS1 Myanmar
$(document).ready(function() {
    $('#pdf-download-button').on('click', function() {
        window.location.href = '/download_zip';
    });

    $('.example-text').click(function() {
        var exampleText = $(this).text();
        $('#barcode-input').val(exampleText);
        generateDataMatrixBarcode(exampleText);
        displayResult(exampleText);
    });

    $('#barcode-input').on('input', function() {
        var inputData = $(this).val();
        if (isURL(inputData)) {
            $('#result').hide();
            inputData = inputData.replace(/<gs>/g, '');
        } else {
            $('#result').show();
        }
        generateDataMatrixBarcode(inputData);
        displayResult(inputData);
    });

    function isURL(input) {
        var pattern = /^(ftp|http|https):\/\/[^ "]+$/;
        return pattern.test(input);
    }
    
    function generateDataMatrixBarcode(data) {
        $.ajax({
            type: 'POST',
            url: '/generate',
            data: {'barcode-data': data},
            success: function(response) {
                var imagePath = response.image_path + '?t=' + new Date().getTime();
                $('#barcode-image').attr('src', imagePath);
                $('#download-button').attr('href', imagePath);
                $('#download-button').show();
                $('#pdf-download-button').show();
            },
            error: function(xhr, status, error) {
                console.log(error);
            }
        });
    }
    function displayResult(data) {
        var pc;
        var sn;
        var lot;
        var exp;
    
        if (data.length === 16) {
            pc = "Product Code: " + data.substring(2);
            exp = "Expire Date: " + formatDate(data.substring(2));
            lot = "Lot: " + data.substring(2);
            sn = "SN: " + data.substring(2);
        } else {
            pc = "Product Code: " + data.substring(2, 16);
            exp = "Expire Date: (Y/M/D): " + formatDate(data.substring(18, 24));
            lot = "Lot: " + data.substring(26, data.indexOf(''));
    
            // Extract all characters after '21' for SN
            var delimiter = '21';
            var delimiterIndex = data.indexOf(delimiter);
    
            if (delimiterIndex !== -1) {
                sn = "SN: " + data.substring(delimiterIndex + delimiter.length);
            } else {
                sn = "SN: " + data.substring(35);
            }
        }
    
        var resultText = pc + "<br>" + exp + "<br>" + lot + "<br>" + sn;
    
        if (resultText.startsWith("Product Code: http")) {
            resultText = "";
        }
    
        $('#result').html(resultText);
    }
    
    
    

    function formatDate(dateString) {
        var year = dateString.substring(0, 2);
        var month = dateString.substring(2, 4);
        var day = dateString.substring(4);
        return year + "-" + month + "-" + day;
    }
});
