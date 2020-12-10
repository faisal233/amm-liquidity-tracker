// Create the namespace instance
let ns = {};

// Create the model instance
ns.model = (function () {
    'use strict';

    // Return the API
    return {
        read_one: function (token_id) {
            let ajax_options = {
                type: 'GET',
                url: `/api/tokens/${token_id}`,
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        read: function () {
            let ajax_options = {
                type: 'GET',
                url: '/api/tokens',
                accepts: 'application/json',
                dataType: 'json'
            };
            return $.ajax(ajax_options);
        },
        create: function (token) {
            let ajax_options = {
                type: 'POST',
                url: '/api/tokens',
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(token)
            };
            return $.ajax(ajax_options);
        },
        update: function (token) {
            let ajax_options = {
                type: 'PUT',
                url: `/api/tokens/${token.token_id}`,
                accepts: 'application/json',
                contentType: 'application/json',
                dataType: 'json',
                data: JSON.stringify(token)
            };
            return $.ajax(ajax_options);
        },
        'delete': function (token_id) {
            let ajax_options = {
                type: 'DELETE',
                url: `/api/tokens/${token_id}`,
                accepts: 'application/json',
                contentType: 'plain/text'
            };
            return $.ajax(ajax_options);
        }
    };
}());

// Create the view instance
ns.view = (function () {
    'use strict';

    let $token_id = $('#token_id'),
        $symbol = $('#symbol'),
        $create = $('#create'),
        $update = $('#update'),
        $delete = $('#delete'),
        $reset = $('#reset');

    // return the API
    return {
        reset: function () {
            $token_id.text('');
            $symbol.val('').focus();
        },
        update_editor: function (token) {
            $token_id.text(token.token_id);
            $symbol.val('').focus();
        },
        build_table: function (tokens) {
            let source = $('#tokens-table-template').html(),
                template = Handlebars.compile(source),
                html;

            // clear the table
            $('.tokens table > tbody').empty();

            // did we get a tokens array?
            if (tokens) {

                // Create the HTML from the template and tokens
                html = template({
                    tokens: tokens
                })

                // Append the html to the table
                $('table').append(html);
            }
        },
        error: function (error_msg) {
            $('.error')
                .text(error_msg)
                .css('visibility', 'visible');
            setTimeout(function () {
                $('.error').fadeOut();
            }, 2000)
        }
    };
}());

// Create the controller
ns.controller = (function (m, v) {
    'use strict';

    let model = m,
        view = v,
        $url_token_id = $('#url_token_id'),
        $token_id = $('#token_id'),
        $symbol = $('#symbol');

    // Get the data from the model after the controller is done initializing
    setTimeout(function () {
        view.reset();
        model.read()
            .done(function (data) {
                view.build_table(data);
            })
            .fail(function (xhr, textStatus, errorThrown) {
                error_handler(xhr, textStatus, errorThrown);
            })

        if ($url_token_id.val() !== "") {
            model.read_one(parseInt($url_token_id.val()))
                .done(function (data) {
                    view.update_editor(data);
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });
        }
    }, 100)

    // generic error handler
    function error_handler(xhr, textStatus, errorThrown) {
        let error_msg = `${textStatus}: ${errorThrown} - ${xhr.responseJSON.detail}`;

        view.error(error_msg);
        console.log(error_msg);
    }

    // Validate input
    function validate(symbol) {
        return symbol !== ""
    }

    // Create our event handlers
    $('#create').click(function (e) {
        let symbol = $symbol.val()

        e.preventDefault();

        if (validate(symbol)) {
            model.create({
                    'symbol': symbol,
                })
                .done(function (data) {
                    model.read()
                        .done(function (data) {
                            view.build_table(data);
                        })
                        .fail(function (xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

            view.reset();

        } else {
            alert('Problem with input');
        }
    });

    $('#update').click(function (e) {
        let token_id = parseInt($token_id.text()),
            symbol = $symbol.val();

        e.preventDefault();

        if (validate(symbol)) {
            model.update({
                    token_id: token_id,
                    symbol: symbol,
                })
                .done(function (data) {
                    model.read()
                        .done(function (data) {
                            view.build_table(data);
                        })
                        .fail(function (xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                })

        } else {
            alert('Problem with symbol input');
        }
        e.preventDefault();
    });

    $('#delete').click(function (e) {
        let token_id = parseInt($token_id.text());

        e.preventDefault();

        if (validate('placeholder')) {
            model.delete(token_id)
                .done(function (data) {
                    model.read()
                        .done(function (data) {
                            view.build_table(data);
                        })
                        .fail(function (xhr, textStatus, errorThrown) {
                            error_handler(xhr, textStatus, errorThrown);
                        });
                    view.reset();
                })
                .fail(function (xhr, textStatus, errorThrown) {
                    error_handler(xhr, textStatus, errorThrown);
                });

        } else {
            alert('Problem with symbolinput');
        }
    });

    $('#reset').click(function () {
        view.reset();
    })
}(ns.model, ns.view));