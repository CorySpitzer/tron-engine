/*****
 * testbot.c
 *
 * This (trivial) bot always moves south.
 *
 * Compile and test run it (with DEBUG 1) :
 *
 *   $ gcc testbot.c tronlib.c -o testbot
 *   $ ./testbot < test_input.maps
 *     // move 0 : ME offset 6 i.e. (1 1) 
 *     //        THEM offset 8 i.e. (1 3) 
 *   3
 *     // move 1 : ME offset 11 i.e. (2 1) 
 *     //        THEM offset 13 i.e. (2 3) 
 *   3
 *   FATAL ERROR:  'width height' not found as expected 
 *
 *
 * where test_input.maps is
 *   5 4        initial position
 *   #####
 *   #1 2#
 *   #   #
 *   #####
 *   5 4        after first move (both move south)
 *   #####
 *   ## ##
 *   #1 2#
 *   #####
 *   .          exit with error here when sizes not found
 *
 * Set DEBUG to 0 when using with a real referee.
 *
 * See ./tronlib.h and trontlib.c for the interface and implemenation.
 * Jim Mahoney | cs.marlboro.edu | Feb 2014 | MIT License
 *******/

#include <stdio.h>
#include "tronlib.h"

#define DEBUG 1

int main(){
  board b;
  int move = 0;
  while (1){
    if (move == 0){
      b = new_board_from_stdin();
    }
    else {
      read_board_from_stdin(b);
    }
    if (DEBUG){
      printf("  // move %i : ME offset %i i.e. (%i %i) \n", 
             move, me(b), row_at(b, me(b)), col_at(b, me(b)));
      printf("  //        THEM offset %i i.e. (%i %i) \n", 
             them(b), row_at(b, them(b)), col_at(b, them(b)));
    }
    move++;
    commit_move(SOUTH);
  }
}

