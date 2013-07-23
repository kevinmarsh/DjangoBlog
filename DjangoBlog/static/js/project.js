function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

$(function() {
    $('.adminFilter input').change(function() {
        // Filter visibility of blog posts and users for the admin
        var filterVal = $(this).val();
        if (filterVal === 'all') {
            $('.published, .unpublished').show();
        } else if (filterVal === 'published') {
            $('.unpublished').hide();
            $('.published').show();
        } else {
            $('.published').hide();
            $('.unpublished').show();
        }
    });
    $('.delete').click(function() {
        // Delete a blog post
        if (confirm('Are you sure you want to delete this post? It cannot be undone.')) {
            $.post(
                $(this).attr('data-deleteLink'),            // URL
                {'postId': $(this).attr('data-postId')},    // Data
                function(data) {                            // Success
                    if (data.result === 'success') {
                        // Django message is set, redirect to homepage
                        window.location.href = $(this).attr('data-homeLink');
                    } else {
                        alert('Oops! Something went wrong.');
                    }
                }
            );
        }
        return false;
    });
});
