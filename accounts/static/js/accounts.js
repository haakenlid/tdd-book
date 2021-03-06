var initialize = function(navigator, user, token, urls){
  $('#id_login').on('click', function(){
    navigator.id.request();
    document.title += ' login!';
  });
  navigator.id.watch({
    loggedInUser: user,
    onlogin: function(assertion){
      $.post(
        urls.login,
        {
          "assertion": assertion,
          "csrfmiddlewaretoken": token
        }
      )
        .done(function() { window.location.reload(); })
        .fail(function() { navigator.id.logout(); });
    },
    onlogout: function(){
      // does nothing yet
    }
  });
};

window.Superlists = {
  Accounts: {
    initialize: initialize
  }
};