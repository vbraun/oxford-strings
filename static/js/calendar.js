

Calendar = function(admin_url) {
    this.url = admin_url;
    jQuery(document).ready(Calendar.prototype.install.bind(this));
}


// Callback to be bound to checkbox "click"
Calendar.prototype.checkbox_activate = function(event) {
    var checkbox = event.target
    var data = {key_id:checkbox.name, active: checkbox.checked};
    console.log(data);
    jQuery.post(this.url, data);
}


// Callback to the "hide" link
Calendar.prototype.hide_link = function(event) {
    console.log('hide', event);
    var key_id = event.target.name
    var data = {key_id:key_id, active:false};
    jQuery.post(this.url, data);
    var divs = jQuery('div#' + key_id);
    divs.hide();
}

// Install callbacks. Called by the ready handler when the dom is ready.
Calendar.prototype.install = function() {
    console.log('Calendar ready')
    var checkbox_cb = this.checkbox_activate.bind(this);
    jQuery('.calendar_event_checkbox').bind('click', checkbox_cb);
    var hide_link_cb = this.hide_link.bind(this);
    jQuery('a.calendar_event_hide_link').click(hide_link_cb);
}



