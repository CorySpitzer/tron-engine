/* 
bot.c
a first attempt at a tron playing bot
sam judson | marlboro college | programming workshop

approach - the bot does a recursive breadth-first search of the spaces surrounding it. it is looking for the space furthest from it that it can safely reach 
before the other bot, and moves in that direction. if there is none (or, more likely, the search is not exhaustive and there are multiple options), then it 
randomly picks one of its equal options.

considerable assistance from jim mahoney
*/

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>
#include <signal.h>
#include "sams_tronlib.h"

/* timer */
#define MOVELENGTH 800000 /* move length is microseconds - .8 sec */

/* boolean */
#define T 1
#define F 0

/* logging */
#define LOGFILE "sams_bot.log"
#define LOGGING 1

FILE* log_file = NULL;

int alarm_caught = F;

void alarm_handler(int sig) {
  alarm_caught = T;
}

/* returns move direction for best move */
int* find_furthest(cell* new_locations, int new_locations_it, int* to_make_array) {
  int i;
  int furthest_dis = 0;
  int furthest_dir = 0;
  int furthest_row = NULL;
  int furthest_col = NULL;

  for (i=0; i<new_locations_it; i++) {
    if (new_locations[i].them_dis > furthest_dis) {
      if (new_locations[i].row == to_make_array[2] && new_locations[i].col == to_make_array[3]) { /* if same cell as previous best move, keep previous direction */
      	furthest_dis = to_make_array[0];
      	furthest_dir = to_make_array[1];
        furthest_row = to_make_array[2];
      	furthest_col = to_make_array[3];
      } else {
	furthest_dis = new_locations[i].them_dis;
	furthest_dir = new_locations[i].me_dir;
	furthest_row = new_locations[i].row;
	furthest_col = new_locations[i].col;
      }
    }
  }

  if (furthest_dis >= to_make_array[1]) {
    to_make_array[0] = furthest_dir;
    to_make_array[1] = furthest_dis;
    to_make_array[2] = furthest_row;
    to_make_array[3] = furthest_col;
  }
    
  return to_make_array;
}

/* sets the direction for a new cell */
cell set_dir(cell new_loc, cell curr_cell, int dir, int level){
  if (level == 1) {
    new_loc.me_dir = dir;
  } else {
    new_loc.me_dir = curr_cell.me_dir;
  }

  return new_loc;
}

/* checks takes a cell and a direction and returns cell in that direction */
cell prospective_move(cell curr_cell, int dir, int level){
  cell new_loc;

  if (dir == 1) {
    new_loc.row = (curr_cell.row - 1);
    new_loc.col = curr_cell.col;
  } else if (dir == 2) {
    new_loc.col = (curr_cell.col + 1);
    new_loc.row = curr_cell.row;
  } else if (dir == 3) {
    new_loc.row = (curr_cell.row + 1);
    new_loc.col = curr_cell.col;
  } else if (dir == 4) {
    new_loc.col = (curr_cell.col - 1);
    new_loc.row = curr_cell.row;
  }

  return set_dir(new_loc, curr_cell, dir, level);
}

/* returns true if cell has not already been reached at this level */
int is_new (cell* new_locations, int new_locations_it, cell new_loc) {
  int i;

  for (i=0; i<new_locations_it; i++) {
    if (new_loc.row == new_locations[i].row && new_loc.col == new_locations[i].col) {
      return F;
    }
  }

  return T;
}

/* for a given cell, see if cells around it are valid moves and haven't been seen before, if so, add to new_locations */
int cell_search(boardp b, cell* new_locations, int new_locations_it, cell curr_cell, cell me_cell, cell them_cell, int level, int to_make_dir) {
  int i, new;
  cell new_loc;

  if (LOGGING) {
    fprintf(log_file,"Currently Checking: %d %d\n", curr_cell.row, curr_cell.col);
  }

  for (i=1; i<=4; i++) {
    new_loc = prospective_move(curr_cell, i, level);

    if (valid_move(b, new_loc)) {
      new_loc.me_dis = distance_between_cells(new_loc, me_cell);
      new_loc.them_dis = distance_between_cells(new_loc, them_cell);
      
      if (LOGGING) {
	fprintf(log_file, "New Loc: %d %d - Me Dis: %d | Them Dis: %d\n", new_loc.row, new_loc.col, new_loc.me_dis, new_loc.them_dis);
      }

      if (new_loc.me_dis <= new_loc.them_dis) {
	new = is_new(new_locations, new_locations_it, new_loc);
	if (new) {
	  new_locations[new_locations_it++] = new_loc;
	} else {
	  if (new_loc.me_dir == to_make_dir) { /* if reach cell from two directions, and one direction is from the previous best move, keep that direction */
	    new_locations[i].me_dir = to_make_dir;
	  }
	}
      }
    }
  }
  
  return new_locations_it;
}

/* determines the max number of cells in the previous level */
int max_prev_loc(int level) {
  if (level == 1) {
    return 1;
  } else {
    return (4 * (level - 1));
  }
}

/* run through prev_locations for new_locations */
int recur_level(boardp b, cell me_cell, cell them_cell, int level, int* to_make_array, cell* prev_locations) {
  int i, prev_locations_count, size_of_prev;
  int new_locations_it = 0;
  cell cell_to_search;
  cell* new_locations;

  size_of_prev = max_prev_loc(level);
  new_locations = calloc(4 * level, sizeof(cell));

  if (LOGGING) {
    fprintf(log_file, "Level: %d\nMe Loc: %d %d\nThem Loc: %d %d\n", level, me_cell.row, me_cell.col, them_cell.row, them_cell.col);
  }

  for (i=0; i<size_of_prev; i++) {
    if (alarm_caught) {
      if (LOGGING) {
	fprintf(log_file, "\n\n!!!Alarm Caught!!!\n\n");
      }
      alarm_caught = F;
      free(prev_locations);
      free(new_locations);
      return to_make_array[0];
    }

    cell_to_search = prev_locations[i];
    if (cell_to_search.me_dis || level == 1) {  /* 0 is either due to it being first level (seeded with me_cell) or off the end of the cells (calloc) */
      new_locations_it = cell_search(b, new_locations, new_locations_it, cell_to_search, me_cell, them_cell, level, to_make_array[0]);
    } 
  }
  
  to_make_array = find_furthest(new_locations, new_locations_it, to_make_array);

  if (LOGGING) {
    fprintf(log_file, "\nBest Move: Dir: %d, Dis: %d - Towards %d %d\n\n", to_make_array[0], to_make_array[1], to_make_array[2], to_make_array[3]);
  }

  if (level < (b -> width * b -> height)) {   /* Allows coverage of the entire board, doesn't allow it to run into memory leaks for small boards */
    free(prev_locations);
    level++;
    return recur_level(b, me_cell, them_cell, level, to_make_array, new_locations);
  } else {
    free(prev_locations);
    free(new_locations);
    return to_make_array[0];
  }

}

void log_move(FILE* log_file, cell me_cell, cell them_cell, int to_make, int move) {
  fprintf(log_file, "Summary:\n\nmove: %d\n", move);
  fprintf(log_file, "\tme position:     %d, %d\n", me_cell.row, me_cell.col);
  fprintf(log_file, "\tthem position:   %d, %d\n", them_cell.row, them_cell.col);
  fprintf(log_file, "\tdecision:           %d\n\n---\n\n", to_make);
}

/* sets the alarm handler */
void set_handler() {
  struct sigaction sa;
  
  sa.sa_handler = alarm_handler;
  sigaction(SIGALRM, &sa, NULL);
}

/* sets the alarm */
void set_timer() {
  struct itimerval timer;
  
  timer.it_value.tv_sec = 0;
  timer.it_value.tv_usec = MOVELENGTH;
  timer.it_interval.tv_sec = 0;
  timer.it_interval.tv_usec = 0;
  
  setitimer(ITIMER_REAL, &timer, NULL);
}

/* sets correct starting attributes for the current position cell */
cell set_me_cell(cell me_cell, cell them_cell) {
  me_cell.me_dis = 0;
  me_cell.me_dir = 0;
  me_cell.them_dis = distance_between_cells(me_cell, them_cell);

  return me_cell;
}

void reset_to_make_array(int* to_make_array) {
  to_make_array[0] = 0;
  to_make_array[1] = 0;
  to_make_array[2] = -1;
  to_make_array[3] = -1;
}

int main() {
  boardp b = new_board();
  cell* move_search_seed;
  cell me_cell, them_cell;
  int move;
  int to_make;
  int to_make_array[4];
  
  if (LOGGING) {
    log_file = fopen(LOGFILE, "w");
    move = 1;
  } 

  set_handler();

  while (1) {
    set_timer();

    read_map(b);
    them_cell = them(b);
    me_cell = me(b);
    me_cell = set_me_cell(me_cell, them_cell);

    move_search_seed = calloc(1, sizeof(cell));
    move_search_seed[0] = me_cell;

    reset_to_make_array(to_make_array);

    to_make = recur_level(b, me_cell, them_cell, 1, to_make_array, move_search_seed);
    fprintf(log_file, "Commiting Move: %d\n\n", to_make);
    commit_move(to_make);
    
    if (LOGGING) {
      log_move(log_file, me_cell, them_cell, to_make, move);
      move++;
    }
  }
  
  return 0;
}
