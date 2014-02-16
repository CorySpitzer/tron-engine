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

void read_map(boardp b);                  /* Modify board in place. */
cell me(boardp b);                        /* Position of ME in map. */
cell them(boardp b);                      /* Position of THEM in map. */
char tile(boardp b, cell c);              /* Char on board at location. */
void commit_move(int direction);          /* Output move to referee. */

void warn(const char* message);           /* Send debug output to stderr. */
void init_error_log(const char* filename);/* Append stderr to filename and */
                                          /* write 1st timestamp line to it. */
