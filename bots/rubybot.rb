#!/usr/bin/env ruby
##################################################
# rubybot.rb
#
# A Tron robot in ruby.
#
# To write your own, all you really ned to change is the TronBot class.
#
# Tested with ruby 1.8.7.
#
# Based on the ruby starter bot and its dependencies,
# from tron.aichallenge.org/starter_packages/ruby_starter_package.zip ,
# which was in turn based on the aichallenge.org Java starter bot.
# (See its COPYING notice at the bottom of the file.)
#
# Jim Mahoney | cs.marlboro.edu | Feb 2014
###################################################

# Directions
NORTH = 1
EAST  = 2
SOUTH = 3
WEST  = 4

# Tiles
FLOOR = ' '
WALL  = '#'
ME    = '1'       # current player
THEM  = '2'       # opponent

# The board position coordinate (i.e. position, location)
# convention is (row, column) or (y,x) pairs 
# where (0,0) top left, for example
#
#    0,0  0,1  0,2
#    1,0  1,1  1,2
#    2,0  2,1  2,2

DIRECTIONS = [NORTH, EAST,  SOUTH, WEST]

# OFFSETS[NORTH] to OFFSETS[WEST] (i.e. [1] to [4])
# are the [dy, dx] change in position.
# (Don't loop over these, since OFFSET[0] is meaningless.
#  Loop over DIRECTIONS instead.)
OFFSETS = [nil, [-1,0], [0,1], [1,0], [0,-1]]

# Output a move to the game referee.
def commit_move(direction)
  # Direction is an integer 1 to 4, i.e. NORTH, EAST, SOUTH, WEST
  # (Using $stdout here explicitly makes sure that this 
  #  works even if (puts, print, p) get redefined.)
  $stdout << direction.to_s + "\n"
  $stdout.flush
end

# A random element from an array.
# The built-in syntax is apparently differently in different versions
# of ruby. If I understand the docs correctly
#   * in versions >= 1.9.1, array.sample picks a random element,
#     an array.sample(n) picks a random subarray.
#   * in version 1.8.7, array.choice picks a single single random element.
#   * in versions before 1.8.7 there isn't a built-in method.
# I see that the RUBY_VERSION global allows me to look at that version string,
# which tempted me to try some tricky conditional class definitions.
# But adding to a base class already seems tricky enough.
# So here I'm just adding an array.random_choice method (which I don't think
# has a name conflict with anything standard), implemented with
# functionality that I think is consistent across many versions,
# and leave it at that.
class Array
  # Return one random element from an array.
  def random_choice
    self[rand(self.size)]
  end
end

# The Map class gets the Tron map from the game engine
# and provides some methods that allow you to look at it.
class Map
  attr_reader :width, :height

  def initialize()
    @width = nil        # integer horizontal map size
    @height = nil       # integer vertical map size
    @tiles = nil        # [@width * @height] array of tiles
    @_me = nil          # cached [row, column] or [y, x] location
    @_them = nil        # ditto
    read_map
  end	

  # Return true if location [y,x] is not within the map boundary.
  def off_map?(location)
    y,x = location
    return (y >= 0 and y < @height and x >= 0 and x < @width)
  end 

  # Return tile (i.e. ' ', '#', '1', or '2') at a location y,x
  def tile(location)
    if off_map?(location)
      return WALL
    else
      y,x = location
      return @tiles[x + y * @width].chr
    end
  end

  # Return first [y,x] location of someone (ME or THEM)
  def find(who)
    i = @tiles.index(who).to_i
    return [i / @width, i % @width]
  end

  # Return [y,x] location of me (i.e. '1') on the map.
  def me
    if @_me == nil then @_me = find(ME) end
    return @_me
  end 

  # Return [y,x] location of them (i.e. '2') on the map.
  def them
    if @_them == nil then @_them = find(THEM) end
    return @_them
  end 

  # Return true if there's a wall at location [y, x].
  def wall?(location)
    return tile(location) == WALL
  end

  # Return true if the location at [y,x] is a floor.
  def floor?(location)
    return tile(location) == FLOOR
  end

  # Return location [y, x] reached after moving in a direction
  # from an origin (default the player's current position).
  def destination(direction, origin = :me)
    if origin == :me then origin = me end
    location = origin.dup
    2.times {|i| location[i] += OFFSETS[direction][i]}
    return location
  end

  # Return list of moves to non-wall (floor or opponent) tiles.
  #   Note that since moves are simultaneous, 
  #   moving into an opponents position (i.e. self.them)
  #   may result in a draw (if they move into you at the same time)
  #   but may also be lose (if they move elsewhere).
  def moves()
    return DIRECTIONS.select {|d| not wall?(destination(d))}
  end

  # Return a string representation of the map.
  def to_string()
    result = ""
    @height.times {|y| result += @tiles[y .. (y+@width-1)] + "\n"}
    return out
  end

  # Get a map from the referee via stdin
  def read_map
    begin
      # read the width and height from the first line
      firstline = $stdin.readline("\n").chomp
      width, height = firstline.split(" ")
      @width = width.to_i
      @height = height.to_i

      ## debugging
      # warn " ** map 1st line: " + 
      #  "line='#{firstline}' width='#{@width}', height='#{@width}'"
			
      # check for properly formatted width, height
      if @height == 0 or @width == 0
	warn "OOPS!: invalid map dimensions in line '#{firstline}'."
	exit(1)
      end
      
      # read the rest of the board into @tiles, removing newlines.
      lines = []
      @height.times do
	       lines += [$stdin.readline("\n").strip]
	     end
      @tiles = lines.join("")

    rescue EOFError => error
      # Got EOF: tournament is finished.
      exit(0)
			
    rescue => error
      # adapted from stackoverflow.com/questions/10050813/
      # is-it-possible-to-get-the-line-number-that-threw-an-error
      warn "Error reading map '#{error.message}'."
      warn "Backtrace = #{error.backtrace}."
      exit(1)
    end
  end

end

# -------------------------------------------------------------- 

class TronBot

  # Return the move for this turn as described by this map.
  #
  # *** Change this method to define your bot's behavior. ***
  #
  def which_move(map)
    # This robot returns a random legal move.
    valid_moves = map.moves
    if valid_moves.size == 0
      return NORTH
    else
      return valid_moves.random_choice
    end
  end

  # Play a game. 
  def run
    while(true)
      map = Map.new()           # get a map from the referee (via stdin)
      move = which_move(map)    # decide what to do
      commit_move(move)         # send the move to the referee (via stdout)
    end
  end

end

# Let 'er rip!
TronBot.new.run

# ----------------------------------------------------------------------

#
# COPYING
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESS OR IMPLIED
# WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
# BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
