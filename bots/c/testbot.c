/*****
 * testbot.c
 *
 * This (trivial) bot always moves south.
 *
 * Compile and test run it (with DEBUG 1) :
 *
 *   $ gcc testbot.c tronlib.c -o testbot
 *   $ ./testbot < test_input.maps
 *     // move 0 : ME at (1 1), THEM at (1 3) 
 *   3
 *     // move 1 : ME at (2 1), THEM at (2 3) 
 *   3
 *   FATAL ERROR:  'width height' not found as expected 
 *
 * where test_input.maps is
 *
 *   5 4        initial position (tiny 5 x 4 board)
 *   #####
 *   #1 2#
 *   #   #
 *   #####
 *   5 4        after first move (both move south, leaving wall trails)
 *   #####
 *   ## ##
 *   #1 2#
 *   #####
 *   .          exit with error here when sizes not found
 *
 * Set DEBUG to 0 when using with a real referee.
 *
 * See ./tronlib.h and trontlib.c for the interface and implemenation.
 * Jim Mahoney | cs.marlboro.edu | Feb 9 2014 | MIT License
 *******/

#include <stdio.h>
#include "tronlib.h"

#define DEBUG 1

int main(){
  boardp b = new_board();
  int move = 0;
  while (1){
    read_map(b);
    if (DEBUG){
      printf("  // move %i : ME at (%i %i), THEM at (%i %i) \n", 
             move, me(b).row, me(b).col, them(b).row, them(b).col);
    }
    move++;
    commit_move(SOUTH);
  }
}

