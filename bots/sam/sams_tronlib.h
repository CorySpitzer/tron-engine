/*******
 * tronlib.h
 * See ./tronlib.c and testbot.c for implementation and usage.
 * Jim Mahoney | cs.marlboro.edu | Feb 9 2014 | MIT License
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

typedef struct _cell cell;                /* position on a board */
struct _cell {
  int row;                                /* vertical position,   0 is top */
  int col;                                /* horizontal position, 0 is left */
  int me_dir;                             /* direction to move from me to cell */
  int me_dis;                             /* distance from cell to me */
  int them_dir;                           /* direction to move from them to cell - to be used with possible AI extension */
  int them_dis;                           /* distance from cell to them */
};

typedef struct _board *boardp;            /* boardp is 'board pointer' */
struct _board {
  int width;
  int height;
  cell _me;                               /* cached position if .row > 0 */
  cell _them;
  char* map;                              /* width*height chars then NULL  */
};
boardp new_board();                       /* its map is not yet allocated */
void init_map(boardp b, int width, int height);
void free_board(boardp b);

void read_map(boardp b);                  /* modifies board in place */
cell me(boardp b);                        /* position of ME in map */
cell them(boardp b);                      /* position of THEM in map */
char tile(boardp b, cell c);              /* what's on the board at position */
void commit_move(int direction);          /* output move to referee */
int valid_move(boardp b, cell to_loc);    /* returns true if move to open space */
int distance_between_cells(cell x, cell y);







