/* the functions are not accessible from the console
see how to do better */
(function($) {

/* search box default front front page and search page*/

var sbox_default = 'Type some keywords...';
var sbox_default2 = 'Search or add keywords ...';

function handleSearchBoxDefault(sbox, sbox_default) {
    if (sbox.get(0)) {
        sbox.bind({
            focus: function() {
                if($(this).attr('value') == sbox_default) {
                    $(this).attr('value', '');
                    $(this).css({'font-style':'normal'});
                }
            },
            blur: function() {
                if($(this).attr('value') == '') {
                    $(this).attr('value', sbox_default);
                    $(this).css({'font-style':'italic'});
                }
            }
        });
        sbox[0].value = sbox_default;
    }
}

handleSearchBoxDefault($('.front_page .search_entry input'), sbox_default);
handleSearchBoxDefault($('.search .search_entry input'), sbox_default2);
handleSearchBoxDefault($('.directory .search_entry input'), sbox_default);

function changeFacetView(fname, fview){
    var query = $('#query').attr('value');
    query = query ? query : '';

    var url = '/load_facet/'+fname+'/'+fview+'?q='+query;
    var container = $('.facet.' + fname + ' ' + '.container');
    var toggle = $('.facet.' + fname + ' ' + '.select_view');

    /*var all_views = getUserPrefs('selected_view');
    all_views[fname] = fview;
    setUserPrefs('selected_view', all_views);*/

    $.ajax({
        url: url,
        success: function(data) {
            container.html(data)
        },
        beforeSend: function() {
            toggle.css('background', 'url(/img/ajax-loader.gif) no-repeat left');
        },
        complete: function(){
            toggle.css('background', 'none');
        }
    });
}

$('.facet .select_view select').change(function(){
    fname = $(this).parent().parent('.facet').attr('class').split(' ')[1]
    fview = $(this).attr('value');
    changeFacetView(fname, fview);
    setUserPrefs('selected_visu.'+fname, fview);
    setUserPrefs('collapsed.'+fname, false);
    $(this).parent().parent('.facet').removeClass('collapsed');
});

$('.facets .facet h4').click(function(){
    facet = $(this).parent();
    fname = facet.attr('class').split(' ')[1];
    fview = facet.find('select option:selected').val();
    facet.find('.container').text('');
    if (facet.hasClass('collapsed')) {
        facet.removeClass('collapsed');
        changeFacetView(fname, fview);
        setUserPrefs('collapsed.'+fname, false);
        setUserPrefs('selected_visu.'+fname, fview);
    }
    else {
        facet.addClass('collapsed');
        setUserPrefs('collapsed.'+fname, true);
    }
});

/* search in all items or current results */
$('.search .search_form input.submit').click(function(){
    var new_query = $('.search_form .search_entry input').attr('value');
    if (new_query && new_query !== sbox_default2) {
        if ($(this).val() == 'Add Keyword')
            $('input[value="all_items"]').val('in_results');
        return true;
    }
    else
        return false;
});

/* switch between instances */
$('select.other_instances').change(function(){
    loc = $(this).attr('value');
    if (loc) {
        window.location = loc;
    }
});

/* get the user preferences */
function getUserPrefs() {
    var prefs = $.cookie('user_pref');
    if (prefs) {
        prefs = JSON.parse(prefs)
    } else {
        prefs = new Object();
    }
    return prefs
}

/* save user preferences for the sessions */
function setUserPrefs(name, value) {
    var prefs = getUserPrefs();
    setPath(prefs, name, value);
    $.cookie('user_pref', JSON.stringify(prefs), {path: '/'});
}

/* toggle a boolean in user pref cookie */
function toggleUserPrefs(name) {
    var value = !(getUserPrefs()[name]);
    setUserPrefs(name, value);
}

/* highlight search terms */
function highlightKeywords() {
    var pattern = $('.highlighter input').attr('value');
    if (pattern) {
        pattern = '\\b(' + pattern + ')s?\\b';
        $('.result').highlight(new RegExp(pattern, 'ig'));
    }
}

function highlightSimilar() {
    $.each($('.result'), function() {
        $(this).highlight($(this).find('.terms_similar').val());
        $(this).find('.highlight').css({background:'#FFEFCF'});
    });
}

function setHighlighting(on, also_similar) {
    var toggle = $('.highlighter span')
    if (on) {
        /*if (also_similar) {
            highlightSimilar();
        }*/
        highlightKeywords();
        toggle.replaceWith('<span class="turned_on" title="Remove highlighting"></span>');
        setUserPrefs('highlighting', true);
    } else {
        $('.result').removeHighlight();
        toggle.replaceWith('<span class="turned_off" title="Highlight search terms"></span>');
        setUserPrefs('highlighting', false);
    }
}

$('.highlighter').click(function(){
    var toggle = $('.highlighter span');
    var also_similar = $('.highlighter #also_similar');
    var on = toggle.hasClass('turned_off');
    setHighlighting(on, also_similar);
});

/* debug search */
$('.toggle_debug_search').click(function(){
    toggleUserPrefs('debug');
});

/* sort by */
$('.sort_by select').change(function(){
    var so = $(this).attr('value');
    var loc = window.location.href;
    loc = loc.replace(/\?.+/, '');
    window.location = loc + '?so=' + so;
});

/* loading user preferences */
function loadUserPrefs() {
    var prefs = getUserPrefs();
    setHighlighting(prefs.highlighting);
}
loadUserPrefs();

/* some useful functions */
function getPath(obj, path) {
    function get(obj, path) {
        return path.length ? get(obj[path[0]], path.slice(1)) : obj
    }
    get(obj, path.split('.'));
}

function setPath(obj, path, val) {
    function set(obj, path, val) {
        (path.length > 1) ? set(obj[path[0]], path.slice(1), val) : (obj[path[0]] = val)
    }
    set(obj, path.split('.'), val);
}

function getUrlVars(name)
{
    var vars = [], hash;
    var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
    for(var i = 0; i < hashes.length; i++)
    {
        hash = hashes[i].split('=');
        vars.push(hash[0]);
        vars[hash[0]] = hash[1];
    }
    if (name)
        return vars[name];
    else
        return vars;
}

})(jQuery);

/* more less */
function addMoreLess() {
    $('.toggle_more').click(function () {
        $(this).hide();
        $(this).next('.more_less').show();
        $(this).next('.more_less').children().last().show();
    });

    $('.toggle_less').click(function () {
        $(this).parent('.more_less').hide();
        $(this).parent('.more_less').prev('.toggle_more').show();
    });
}
addMoreLess();

Array.max = function( array ){
    return Math.max.apply( Math, array );
};
Array.min = function( array ){
    return Math.min.apply( Math, array );
};

/* infinite scroll *//*
$(window).scroll(function(){
    if  ($(window).scrollTop() == $(document).height() - $(window).height()){
        loadMoreResults();
    }
});

function loadMoreResults() {
    var start = $('#start_scroll');
    start.val(parseInt(start.val()) + 10);

    var query = $('#query').attr('value');
    query = query ? query : '';

    var url = '/load_results/?q='+query + '&s=' + start.val();
    var container = $('.results');
    var toggle = $('.stats');

    $.ajax({
        url: url,
        success: function(data) {
            container.append(data)
        },
        beforeSend: function() {
            toggle.css('background', 'url(/img/ajax-loader.gif) no-repeat left');
        },
        complete: function(){
            toggle.css('background', 'none');
        }
    });
};*/

function drawRose(element, fobj, color, facet_name, opts) {
    var f = fobj.matches;

    var data = [];
    var labels = [];
    var tooltips = [];
    for (i=0; i<f.length; i++) {
        if (!f[i]['@selected']) {
            var count = f[i]['@count'];
            var term = f[i]['@term'];
            var tooltip = term + ' - ' + count;
            /*data.push(Math.log(count));*/
            data.push(count);
            labels.push(term);
            tooltips.push(tooltip);
        }
    }

    if (data.length == 0) {
        for (i=0; i<f.length; i++) {
            var count = f[i]['@count'];
            var term = f[i]['@term'];
            var tooltip = term + ' - ' + count;
            /*data.push(Math.log(count));*/
            data.push(count);
            labels.push(term);
            tooltips.push(tooltip);
        }
    }

    var rose = new RGraph.Rose(element.id, data);

    rose.Set('chart.colors', [color]);
    rose.Set('chart.colors.alpha', 0.4);

    rose.Set('chart.labels', labels);
    rose.Set('chart.labels.position', 'center');

    rose.Set('chart.tooltips', tooltips);
    rose.Set('chart.tooltips.event', 'onmousemove');

    /*rose.Set('chart.zoom.factor', 20);*/
    rose.Set('chart.gutter.left', 0);
    rose.Set('chart.gutter.right', 0);
    rose.Set('chart.gutter.top', 25);
    rose.Set('chart.gutter.bottom', 25);
    /*rose.Set('chart.margin', 0);*/

    rose.Set('chart.text.size', 7);
    /*rose.Set('chart.ymax', Array.max(data)/2);*/
    rose.Set('chart.ymax', Array.max(data));
    rose.Set('chart.labels.axes', 'e');
    rose.Set('chart.scale.round', false);

    RGraph.Register(rose);
    /*var query = $('#query').attr('value');
    query = query ? query : '';*/
    rose.canvas.onclick = function (e)
    {
        RGraph.FixEventObject(e);
        RGraph.Redraw();

        var canvas  = e.target;
        var context = canvas.getContext('2d');
        var obj     = canvas.__object__;
        var segment = obj.getSegment(e);

        if (segment) {
            var val = f[segment[6]];
            /*var nquery = '(@' + facet_name + ' ' + val['@term'] + ')';
            var url = '/search?q=' + query + ' ' + nquery;*/
            var url = '/search/' + val['@url'];
            window.location = url;
            e.stopPropagation();
        }
    }
    if (opts.animate) {
        RGraph.Effects.Rose.Grow(rose);
    }
    else {
        rose.Draw();
    }
}

/*function drawPie(element, fobj) {
    // Create and populate the data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', fobj.name);
    data.addColumn('number', 'Scores');
    data.addRows(fobj.matches.length);

    for (i=0; i<7; i++) {
        data.setValue(i, 0, fobj.matches[i].@term);
        data.setValue(i, 1, fobj.matches[i].@count);
    }

    // Create and draw the visualization.
    new google.visualization.PieChart(element).
        draw(data, {
            pieSliceText: 'label',
            legend: 'none',
            colors: ['#EFF5FF'],
            pieSliceTextStyle: {color:'blue', fontSize:13},
            chartArea: {left:0, top:0, width:'100%', height:'100%'},
            height: 270,
        });
}*/

/*function drawCumulus(element, fobj) {
    // Create and populate a data table.
    var data = new google.visualization.DataTable();
    data.addColumn('string', 'Tag');
    data.addColumn('string', 'URL');
    data.addColumn('number', 'Font size');
    data.addRows(fobj.matches.length);

    for (i=0; i<fobj.matches.length; i++) {
        data.setCell(i, 0, fobj.matches[i].@term);
        data.setCell(i, 1, '/search?q=@' + fobj.name + ' ' + fobj.matches[i].@term);*/
/*        data.setCell(i, 1, 'http://www.google.com');
        data.setCell(i, 2, 12);*/
/*    }

    new gviz_word_cumulus.WordCumulus(element).
        draw(data, {
            text_color: '#0000CC',
            speed: 50,
            width: 300,
            height: 225
        });

    // a bit of ajustement
    $(element).css('text-align', 'center');
}*/

