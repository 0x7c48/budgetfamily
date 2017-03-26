faForm.addFieldConverter(function($el, name) {
    if (name != 'select2-choices') {
        return false;
    }

    var perms = $el.attr('data-choices').split(',');
    var data = perms.map(function(perm) {
        return {id: perm, text: perm};
    });

    $el.select2({
        width: 'resolve',
        data: data,
        multiple: true
    });
    return true;
});
