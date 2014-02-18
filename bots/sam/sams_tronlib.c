/*******
 * tronlib.c
 * See ./tronlib.h and testbot.c for the interface and usage.
 * Jim Mahoney | cs.marlboro.edu | Feb 9 2014 | MIT License
 *****/

#include "sams_tronlib.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void _fatal_error(char* error_message){
    printf("FATAL ERROR: %s \n", error_message);
    exit(1);
}

void read_line(char* buffer, char* error_message){
  /* copy a line from stdin to buffer */
  char* status;
  size_t length;
  buffer[0] = 0;  /* initialize to length 0 */
  status = fgets(buffer, MAX_BOARD_WIDTH+1, stdin);
  length = strlen(buffer);
  if (status == NULL || length == 0 || length > MAX_BOARD_WIDTH){
    _fatal_error(error_message);
  }
}

boardp new_board(){
  boardp b = malloc(sizeof(struct _board));
  b->width = b->height = b->_me.row = b->_them.row = -1;
  return b;
}

void read_map(boardp b){
  /* The bot reads the map from stdin on each turn,
     with the width and height on the first line,
     and the map on the following height x width lines, like this :
        5 4               // 5 columns by 4 rows
        #####             // row 0, column 0 to 4
        #1 2#             // 1 is "me", 2 is "them"
        #   #             // # is wall
        #####
   */
  char buffer[MAX_BOARD_WIDTH+2];
  int width, height, status, i;
  read_line(buffer, " 'width height' input line could not be read");
  status = sscanf(buffer, "%d %d", &width, &height);
  if (status != 2){
    _fatal_error(" 'width height' not found as expected");
  }
  if (b->width == -1){             /* 1st time: initialize board map */
    b->map = malloc(width * height + 1);
    b->width = width;
    b->height = height;
    b->map[0] = 0;                /* set to zero length string */
  }
  if (width != b->width || height != b->height){
    _fatal_error("inconsistent width or height");
  }
  for (i=0; i<height; i++){
    read_line(buffer, "could not read board row");
    memcpy(b->map + i*width, buffer, width);
  }
  b->map[width * height] = 0;     /* make map null terminated */
  b->_me.row = b->_them.row = -1;  /* clear cached values */
}

void init_map(boardp b, int width, int height){
  if (width < 0 || height < 0){
    _fatal_error("illegal width or height in init_map()");
  }
  if (b->width != -1){  /* map allocated ? */
    free(b->map);
  }
  b->map = malloc(width * height + 1);
  b->width = width;
  b->height = height;
  b->map[0] = 0;                /* map initilized to zero length string */
}

void free_board(boardp b){
  if (b->width != -1){  /* map allocated ? */
    free(b->map);
  }
  free(b);
}

char tile(boardp b, cell c){
  if (c.row > b->height || c.col > b->width){
    return '?';   /* out of bounds error */
  }
  else {
    return b->map[b->width * c.row + c.col];
  }
}

cell find(boardp b, char what){
  int i;
  cell c;
  if (b->width < 0){
    _fatal_error("find() called on board without map");
  }
  for (i=0; i< b->width * b->height; i++){
    if (b->map[i] == what){
      c.row = i / b->width;
      c.col = i % b->width;
      return c;
    }
  }
  _fatal_error("find() failed");
}

cell me(boardp b){
  if (b->_me.row < 0){
    b->_me = find(b, ME);
  }
  return b->_me;
}

cell them(boardp b){
  if (b->_them.row < 0){
    b->_them = find(b, THEM);
  }
  return b->_them;
}

void commit_move(int direction){
  printf("%i\n", direction);
  fflush(stdout);
}

int distance_between_cells(cell x, cell y) {
  return abs(x.row - y.row) + abs(x.col - y.col);
}

int valid_move(boardp b, cell to_loc){
  if (tile(b, to_loc) == WALL || tile(b, to_loc) == THEM || tile(b, to_loc) == ME) {
    return 0;
  } else {
    return 1;
  }
}

