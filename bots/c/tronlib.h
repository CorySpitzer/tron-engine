/*******
 * tronlib.h
 * See ./tronlib.c and testbot.c for implementation and usage.
 * Jim Mahoney | cs.marlboro.edu | Feb 2014 | MIT License
 *****/

#define NORTH 1
#define EAST  2
#define SOUTH 3
#define WEST  4

#define FLOOR ' '
#define WALL  '#'
#define ME    '1'
#define THEM  '2'

#define MAX_BOARD_WIDTH 128

typedef struct _board *board;
struct _board {
  int width;
  int height;
  int _me;                                /* if >= 0, offset to ME in data */
  int _them;                              /* if >= 0, offset to THEM in data */
  char* data;                             /* width*height chars then NULL  */
};

board new_board(int width, int height);   /* data allocated but uninitialized */
board new_board_from_stdin();             /* read in a tron map */
void read_board_from_stdin(board b);      /* read map; modify board in place */
void free_board(board b);

int me(board b);                          /* offset to ME in data */
int them(board b);                        /* offset to THEM in data */
char tile(board b, int offset);

int row_at(board b, int offset);          /* convert offset to row */
int col_at(board b, int offset);          /* convert offset to col */
int offset_at(board b, int row, int col); /* convert row,col to offset */

void commit_move(int direction);          /* output move to referee */








