/*****
 * testbot.c
 *
 * This (trivial) bot always moves south.
 *
 * Compile and test run it (with DEBUG 1) :
 *
 *   $ gcc testbot.c tronlib.c -o testbot
 *   $ ./testbot < test_input.maps
 *   3
 *   3
 *   FATAL ERROR:  'width height' not found as expected 
 *
 * And then look in the log file for warn() and stderr messages.
 *
 *   $ tail /var/www/csmarlboro/tron/logs/you.txt
 *   # or whatever your log file is. 
 *   # The "less" command is more flexible than tail, type > to go the end.
 *
 * The input file test_input.maps is
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

/* --- debugging ---
 * Seeing what's going wrong with these bots can be tricky,
 * since (a) the bot protocol uses stdout, so doing anything else
 * there gets in the way, and (b) the bot will be run by the referee
 * not invoked by you.
 *
 * tronlib.h includes init_error_log(filename) and warn(message),
 * which (a) appends stderr to a file, and (b) sends a message to stderr.
 *
 * The log filename should be an absolute path since the bot may be
 * invoked from a different directory.  And it should be world
 * writeable, since the referee invokes the bot and so it needs access.
 *
 * On csmarlboro.org a good folder is /var/www/csmarlboro/tron/logs/
 * which has permissions allowing anyone to create a file, e.g.
 *
 *  $ ssh user@csmarlboro.org      # substitute your username for user
 *  $ cd /var/www/csmarlboro/tron/logs/
 *  $ touch user.txt               # ditto
 *  $ chmod o+w user.txt           # ditto
 *
 * and edit the logfilename below to match.
 */

/* Set this to 1 to enable debugging to the logfile. */
#define DEBUG 1
#define LOGFILE "/var/www/csmarlboro/tron/logs/you.txt"

int main(){
  boardp b = new_board();
  int move = 0;
  char error_message[128];
  if (DEBUG) init_error_log(LOGFILE);
  while (1){
    read_map(b);
    if (DEBUG){
      sprintf(error_message, " move %i : ME at (%i %i), THEM at (%i %i) ", 
	      move, me(b).row, me(b).col, them(b).row, them(b).col);
      warn(error_message);
    }
    move++;
    commit_move(SOUTH);
  }
}

