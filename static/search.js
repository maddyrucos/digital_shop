$(document).ready(function() {
    $('#search-results').hide()
    $('#search-input').on('input', function() {
        var query = $(this).val();
        if (query.length > 1) {
            $.ajax({
                url: '/search/',
                data: {
                    'q': query
                },
                dataType: 'json',
                success: function(data) {
                    console.log(data)
                    var results = data.results;
                    var html = '';
                    if (results.length > 0) {
                        html += '<ul>';
                        $('#search-results').show()
                        for (var i = 0; i < results.length; i++) {
                            html += '<li><a href="/product/' + results[i].id + '/">' + results[i].name + '</a></li>';
                        }
                        html += '</ul>';
                    } else {
                        html += '<p>No results found.</p>';
                    }
                    $('#search-results').html(html);
                }
            });
        } else {
            $('#search-results').html('').hide();
        }
    });
});