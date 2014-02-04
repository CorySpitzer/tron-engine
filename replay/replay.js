/* replay.js
 * adapted from http://tron.aichallenge.org/visualizer.php?game_id=3355177 
 * Jim Mahoney | cs.marlboro.edu
 * 
 * URL arguments (i.e. replay.html?game_id=2&FPS=8)
 *       game_id      the game to be replayed is ../games/<game_id>.tron ; default 2
 *       FPS          playback frames (moves) per second; default 4
 */

var w, h, frame, board, _board, diffs, p1pos, p2pos;
var loaded, play_timeout;
var http;

var frame_time;       // in msec
var game_id;

var default_FPS = 4;      // frames per second
var default_game_id = 2;  // which points to the url ../games/2.tron exists.

window.onload = load;

function load() {
    loaded = false;
    
    // Check if we should bother loading
    var simspace = document.getElementById('simspace');
    var controls = document.getElementById('controls');
    if (!simspace || !controls) return;

    var FPS = get_url_param('FPS') || default_FPS;
    frame_time = 1000.00 / FPS;

    game_id = get_url_param('game_id') || default_game_id;

    playpause();
    
    var game_url = '../games/' + game_id + '.tron';

    //if (game_id) {
    //    //url = 'csclub.uwaterloo.ca/contest/generate_game_summary.php?game_id=' + gameid;
    //    //url = 'generate_game_summary.php?game_id=' + gameid;
    //    //alert(url);
    //    url = 
    //} else
    //    url = 'test.txt';
    
    http = new XMLHttpRequest();
    http.open("GET", game_url, true);
    http.onreadystatechange = _parse_load;
    http.send(null);
}

function build_initial() {
    diffs = new Array();
    diffs[0] = new Array();
    diffs[0][0] = new Array(); // this should so not be necessary
    diffs[0][1] = new Array();
    p1pos = new Array();
    p2pos = new Array();
    build_board_arrays();
    build_empty_board();
    build_backup_board();
    build_canvas();
}

function build_board_arrays() {
    var x, y;
    board = new Array();
    _board = new Array();
    for (y = 0; y < h; y++) {
        board[y] = new Array();
        _board[y] = new Array();
    }
}

function build_empty_board() {
    var x, y;
    for (y = 0; y < h; y++)
        for (x = 0; x < w; x++) {
            _board[y][x] = '#';
        }
}

function build_backup_board() {
    var x, y;
    for (y = 0; y < h; y++)
        for (x = 0; x < w; x++) {
            _board[y][x] = board[y][x];
        }
}

function symbol_to_style(symbol) {
    switch (symbol) {
    case ' ':
        return 'empty';
    case '#':
        return 'wall';
    case '1':
        return 'player1';
    case '2':
        return 'player2';
    default:
        return 'empty';
    }
}

function build_canvas() {
    var simspace = document.getElementById('simspace');
    while (simspace.hasChildNodes()) {                  // remove old stuff
        simspace.removeChild(simspace.firstChild);   
    }
    var canvas = document.createElement('table');
    canvas.setAttribute('cellspacing', '0');
    canvas.setAttribute('cellpadding', '0');
    canvas.setAttribute('id', 'canvas');
    var row, cell, x, y;
    for (y = 0; y < h; y++) {
        row = document.createElement('tr');
        for (x = 0; x < w; x++) {
            cell = document.createElement('td');
            cell.setAttribute('class', symbol_to_style('empty'));
            row.appendChild(cell);
        }
        canvas.appendChild(row);
    }
    simspace.appendChild(canvas);
}

function draw_canvas() {
    var canvas = document.getElementById('canvas');
    var row = canvas.getElementsByTagName('tr');
    var cell;
    for (var y = 0; y < h; y++) {
        cell = row[y].getElementsByTagName('td');
        for (var x = 0; x < w; x++) {
            cell[x].setAttribute('class', symbol_to_style(board[y][x]))
        }
    }
}

// data is playerdata {x, y, dir, sym}
function update_canvas(data) {
    var x = data[0];
    var y = data[1];
    var dir = data[2];
    var sym = data[3];
    var cell = document.getElementById('canvas').getElementsByTagName('tr')[y].getElementsByTagName('td')[x];
    cell.setAttribute('class', symbol_to_style(sym));;
    cell.innerHTML = dir;
}

// data is playerdata {x, y, dir, sym}
// update, true if draw update
function update_frame(data) {
    var x = data[0];
    var y = data[1];
    var n = data[3];
    board[y][x] = n;
    update_canvas(data); 
}

// data is playerdata {x, y, dir, sym}
function move_dir(data) {
    var newdata = new Array();
    var x = data[0];
    var y = data[1];
    var dir = data[2];
    var sym = data[3];
    
    newdata[3] = sym;
    
    switch (dir) {
    case 'N':
        newdata[0] = x;
        newdata[1] = y - 1;
        newdata[2] = '\u25b2';
        return newdata;
    case 'E':
        newdata[0] = x + 1;
        newdata[1] = y;
        newdata[2] = '\u25b6';
        return newdata;
    case 'S':
        newdata[0] = x;
        newdata[1] = y + 1;
        newdata[2] = '\u25bc';
        return newdata;
    case 'W':
        newdata[0] = x - 1;
        newdata[1] = y;
        newdata[2] = '\u25c0';
        return newdata;
    default:
        newdata[0] = x;
        newdata[1] = y;
        newdata[2] = '\u25a0';
        return newdata;
    }
}

// dir = +/- 1, (-1 -> backwards
function do_diff_dir(dir) {
    /*if ((frame == diffs.length - 1 && dir > 0) || (frame == 0 && dir < 0))
      return;*/
    
    frame += dir;
    
    if (frame > diffs.length - 1)
        frame = diffs.length - 1;
    if (frame < 0)
        frame = 0;
    
    if ((frame >= 0 && dir < 0) || ((frame < diffs.length && dir > 0 && frame != 0))) {
        // data is playerdata {x, y, dir, sym}
        var p1dat, p2dat;
        var oldf = frame - dir;
        p1dat = diffs[oldf][0];
        p2dat = diffs[oldf][1];
        
        if (dir < 0) {
            p1dat = build_data(p1dat[0], p1dat[1], p1dat[2], p1dat[3]);
            p1dat[2] = '';
            p1dat[3] = _board[p1dat[1]][p1dat[0]];
            
            p2dat = build_data(p2dat[0], p2dat[1], p2dat[2], p2dat[3]);
            p2dat[2] = '';
            p2dat[3] = _board[p2dat[1]][p2dat[0]];
            
            update_frame(p1dat);
            update_frame(p2dat);
        } else {
            p1dat = build_data(p1dat[0], p1dat[1], p1dat[2], p1dat[3]);
            p1dat[2] = '';
            p2dat = build_data(p2dat[0], p2dat[1], p2dat[2], p2dat[3]);
            p2dat[2] = '';
            
            update_frame(p1dat);
            update_frame(p2dat);
        }
    };
    
    p1dat = diffs[frame][0];
    p2dat = diffs[frame][1];
    
    update_frame(p1dat);
    update_frame(p2dat);
}

function set_player_name(n, _name, winner) {
    // winner is '1', '2', or 'D'
    var cell = document.getElementById('name' + n);
    _name = _name.replace('bots/', '')   // strip bots folder if present
    var text = _name;
    if (n == winner){
	text += ' (winner)'
    }
    if (winner == 'D' && n == 2){
	text += '&nbsp;&nbsp;&nbsp;(draw)'
    }
    cell.innerHTML = text + '&nbsp';
}

function show_error(err) {
    alert(err || "An unknown error occurred.");
}

// source: gup at http://www.netlobo.com/url_query_string_javascript.html
function get_url_param(name){
    name = name.replace(/[\[]/,"\\\[").replace(/[\]]/,"\\\]");
    var regexS = "[\\?&]"+name+"=([^&#]*)";
    var regex = new RegExp( regexS );
    var results = regex.exec( window.location.href );
    if(results != null)
        return results[1];
}

function build_data(x, y, dir, sym) {
    var data = new Array();
    data[0] = x;
    data[1] = y;
    data[2] = dir;
    data[3] = sym;
    return data;
}

/* The original file format was http://csclub.uwaterloo.ca/~pgpaskar/sim/fileformat.txt
   Now modified to include a winner in last field before final '+OK'. An example created with
      $ ./engines/round.py --replay=out.tron -B maps/empty-room.txt bots/randbot.py bots/randbot.py
   is
+OK|15 15|###############
#1            #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#             #
#            2#
###############
|bots/randbot.py 1|bots/randbot.py 2|EWEWENSNWEWSWESNENENSWWSWWSNSWSSEWSSWSSWENSWWSSSSWENENENSEENNENNNWNNWWWWNWNNNW|D|+OK
*/
function parse_load(raw) {
    raw = raw.split('|');
    
    if (raw.length < 2 || raw[0] != '+OK') {
        if (raw.length > 1 && raw[0] == '+ERR')
            show_error(raw[1]);
        else
            show_error('Error loading game file.');
        return;
    }
    
    var ndx = 1;
    
    var size = raw[ndx++].split(' ');
    w = size[0];
    h = size[1];
    
    build_initial();
    
    // diffs are in data format:
    // data is playerdata {x, y, dir, sym}
    
    var mapdata = raw[ndx++].split('\n');
    
    var x, y, cell;
    
    for (y = 0; y < h; y++) {
        cell = mapdata[y].split('');;
        for (x = 0; x < w; x++) {
            board[y][x] = cell[x];
            _board[y][x] = cell[x];
            
            if (cell[x] == '1') {
                diffs[0][0] = build_data(x, y, '1', '1');
            } else if (cell[x] == '2') {
                diffs[0][1] = build_data(x, y, '2', '2');
            }
        }
    }
    
    // set game name
    document.getElementById('gamename').innerHTML = "game_id '" + game_id  + "' &nbsp; : &nbsp;";

    var player1 = raw[ndx++];
    var player2 = raw[ndx++];
    
    var moves = raw[ndx++];
    var dir, data;
    var f = 0;
    var mf = 0;
    
    while (true) {
        f++;
        dir = moves[mf++];
        
        if (mf > moves.length - 1)
            break;
        
        if (!dir) {
            show_error("File ended unexpectedly<br>Game data may be incomplete!");
            break;
        }
        
        diffs[f] = new Array();
        diffs[f][0] = move_dir(build_data(diffs[f - 1][0][0], diffs[f - 1][0][1], dir, diffs[f - 1][0][3]));
        
        dir = moves[mf++];
        diffs[f][1] = move_dir(build_data(diffs[f - 1][1][0], diffs[f - 1][1][1], dir, diffs[f - 1][1][3]));
    }

    var winner = raw[ndx++];
    set_player_name(1, player1, winner);
    set_player_name(2, player2, winner);
    
    if (raw[ndx++] == '+ERR') {
        show_error(raw[ndx++] + "<br>Game data may be incomplete!");
        return;
    }
    
    draw_canvas();
    
    loaded = true;
    frame = -1;
    forward();
}

function _parse_load() {
    if (http.readyState == 4)
        parse_load(http.responseText);
}


function playpause() {
    if (play_timeout)
        clearTimeout(play_timeout);
}

function forward() {
    do_diff_dir(1);
}
function _forward() {
    if (!loaded) return;
    playpause();
    forward();
}

function backward() {
    do_diff_dir(-1);
}
function _backward() {
    if (!loaded) return;
    playpause();
    do_diff_dir(-1);
}

function playforward() {
    forward();
    if (frame < diffs.length - 1)
        play_timeout = setTimeout(playforward, frame_time);
}
function _playforward() {
    if (!loaded) return;
    playpause();
    playforward();
}

function playbackward() {
    backward();
    if (frame > 0)
        play_timeout = setTimeout(playbackward, frame_time);
}
function _playbackward() {
    if (!loaded) return;
    playpause();
    playbackward();
}

function _gotostart() {
    if (!loaded) return;
    playpause();
    
    while (frame > 0) {
        do_diff_dir(-1);
    }
}
function _gotoend() {
    if (!loaded) return;
    playpause();
    
    while (frame < diffs.length - 1) {
        do_diff_dir(1);
    }
}

