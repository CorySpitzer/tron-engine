/*******
 * tronlib.c
 * See ./tronlib.h and testbot.c for the interface and usage.
 * Jim Mahoney | cs.marlboro.edu | Feb 2014 | MIT License
 *****/

#include "tronlib.h"
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

board new_board(int width, int height){
  board b = malloc(sizeof(struct _board));
  b->width = width;
  b->height = height;
  b->_me = -1;
  b->_them = -1;
  b->data = malloc(width*height+1);
  return b;
}

board new_board_from_stdin(){
  /* The tron board format is e.g.
       5 4
       #####
       #1 2#
       #   #
       #####
     where the first line gives the width and height,
     and the following (height) lines have (width) characters.
   */
  char buffer[MAX_BOARD_WIDTH+2];
  board b;
  int width, height, status, i;
  read_line(buffer, " 'width height' input line could not be read");
  status = sscanf(buffer, "%d %d", &width, &height);
  if (status != 2){
    _fatal_error(" 'width height' not found as expected");
  }
  b = new_board(width, height);
  for (i=0; i<height; i++){
    read_line(buffer, "could not read a board row");
    memcpy(b->data + i*width, buffer, width);
  }
  b->data[width * height] = 0; /* make data null terminated */
  return b;
}

void read_board_from_stdin(board b){
  char buffer[MAX_BOARD_WIDTH+2];
  int width, height, status, i;
  read_line(buffer, " 'width height' input line could not be read");
  status = sscanf(buffer, "%d %d", &width, &height);
  if (status != 2){
    _fatal_error(" 'width height' not found as expected");
  }
  if (width != b->width || height != b->height){
    _fatal_error("inconsistent width or height");
  }
  for (i=0; i<height; i++){
    read_line(buffer, "could not read board row");
    memcpy(b->data + i*width, buffer, width);
  }
  b->data[width * height] = 0; /* make data null terminated */
  b->_me = -1;                 /* clear cached values */
  b->_them = -1;
}

void free_board(board b){
  free(b->data);
  free(b);
}

char tile(board b, int offset){
  return b->data[offset];
}

int find(board b, char what){
  int i;
  for (i=0; i< b->width * b->height; i++){
    if (b->data[i] == what){
      return i;
    }
  }
  _fatal_error("find() failed");
}

int me(board b){
  int i, where;
  if (b->_me >= 0){
    return b->_me;
  }
  else {
    where = find(b, ME);
    b->_me = where;
    return where;
  }
}

int them(board b){
  int i, where;
  if (b->_them >= 0){
    return b->_them;
  }
  else {
    where = find(b, THEM);
    b->_them = where;
    return where;
  }
}

int row_at(board b, int offset){
  return offset / b->width;
}

int col_at(board b, int offset){
  return offset % b->width;
}

int offset_at(board b, int row, int col){
  return row * b->width + col;
}

void commit_move(int direction){
  printf("%i\n", direction);
  fflush(stdout);
}

