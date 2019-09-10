import numpy as np
import scipy as sp
import seaborn as sns
import sys

sys.setrecursionlimit(10000)

class SandPile():
    """SandPile class
    """

    def __init__(self, width, height, threshold=4):
        """Initialize a sandpile with the specified width and height.


        """
        self.width = width
        self.height = height
        self.threshold = threshold

        self.grid = np.zeros((width, height), dtype=int)

        # We may want to keep track of the overall mass of the sand pile
        # overtime.  The following array will store the masses at each time
        # step (so that `len(self.mass_history)` is equal to the number of time
        # steps the sand pile has been running).
        self.mass_history = []
        # You probably will want to define other attributes to store statistics.

        # It is good practice to define *all* attributes in the `__init__`
        # function, even if they get redefined later.  You may want to define
        # variables which are used to keep track of avalanches.
        self.time = 0
        self.topples = 0
        self.area = []
        self.loss = 0
        self.length = np.zeros((width, height), dtype=int)

    def drop_sand(self, n=1, site=None):
        """Add `n` grains of sand to the grid.  Each grains of sand is added to
        a random site.

        This function also increments the time by 1 and update the internal
        `mass_history`

        Parameters
        ==========

        n: int

          The number of grains of sand of drop at this time step.  If left
          unspecified, defaults to 1.

        site:

          The site on which the grain(s) of sand should be dropped.  If `None`,
          a random site is used.

        """

        if not np.any(site):

            x_coordinates = np.random.randint(0, self.width,(1,n), int)[0]
            y_coordinates = np.random.randint(0, self.height,(1,n), int)[0]

            coordinates = np.array((x_coordinates, y_coordinates)).T

            for x, y in coordinates:

                self.grid[x][y] += 1

        else:

            self.grid[site[0], site[1]] += 1


        self.mass_history = np.append(self.mass_history, n)
        self.time += 1

        # VERY USEFUL DEBUG LOOK AT EACH GRID
        # print(f"grid now:")
        # print(f"{self.grid}")


    def mass(self):
        """Return the mass of the grid."""

        return np.sum(self.grid)

    def topple(self, site):
        """Topple the specified site"""

        x = site[0]
        y = site[1]

        ############ CORNERS
        if x == 0 and y == 0:

            self.grid[x+1][y] += 1
            self.grid[x][y+1] += 1

        elif x == 0 and y == (self.width - 1):

            self.grid[x+1][y] += 1
            self.grid[x][y-1] += 1

        elif x == (self.height-1) and y == 0:

            self.grid[x-1][y] += 1
            self.grid[x][y+1] += 1

        elif x == (self.height-1) and y == (self.width - 1):

            self.grid[x][y-1] += 1
            self.grid[x-1][y] += 1

        ############# EDGES
        elif x==0:

            self.grid[x+1][y] += 1
            self.grid[x][y+1] += 1
            self.grid[x][y-1] += 1

        elif y==0:

            self.grid[x-1][y] += 1
            self.grid[x+1][y] += 1
            self.grid[x][y+1] += 1

        elif x==(self.height - 1):

            self.grid[x-1][y] += 1
            self.grid[x][y+1] += 1
            self.grid[x][y-1] += 1

        elif y==(self.width - 1):

            self.grid[x-1][y] += 1
            self.grid[x+1][y] += 1
            self.grid[x][y-1] += 1
        else:
            self.grid[x-1][y] += 1
            self.grid[x+1][y] += 1
            self.grid[x][y+1] += 1
            self.grid[x][y-1] += 1


    def sand_loss(self, site):
        corners = [(0, 0), (0, self.width - 1), (self.height - 1, 0), (self.height - 1, self.width - 1)]
        edges = [0, self.width-1, self.height-1]
        amount_before = self.grid[site]

        sand_lost = 0

        if site in corners and amount_before > 2:
            sand_lost = sand_lost + amount_before - 2


        elif site[0] in edges or site[1] in edges and amount_before > 3:
            sand_lost = sand_lost + amount_before - 3

        return sand_lost

    def check_stabilised(self, old, n=1):

        return old == (self.topples - n)


    def avalanche(self, n=1):
        """Run the avalanche causing all sites to topple and store the stats of
        the avalanche in the appropriate variables.

        """
        centre = [int(self.grid.shape[0]/2), int(self.grid.shape[1]/2)]

        # keep dropping sand until there's a topple.
        if self.topples == 0 and np.amax(self.grid) < 4:

            self.drop_sand(n)
            self.time += 1

            np.append(self.mass_history, self.mass())


        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):

                if self.grid[x,y] >= 4:


                    self.topple((x,y))


                    site = (x, y)

                    # Update avalanche parameters

                    # Keep track of the number of topples,

                    self.topples += 1

                    self.time += 1

                    # sand lost
                    self.loss += self.sand_loss(site)

                    # Now delete sand at toppling site. It is important to do this
                    # only after calling sand_loss
                    self.grid[site] -= 4

                    np.append(self.mass_history, self.mass())

                    #print(self.grid)

                    # unique area toppled
                    if site not in self.area:
                        self.area.append(site)

                    # # Print off grids
                    # print("\n--------------------")
                    # print(f"for site {site}")
                    # print(self.grid)
                    # print(f"I lost {self.loss} so far")


                    # Recur. This might be a bad idea.
                    #self.avalanche()

                # At the end of the grid,
                elif x==(self.grid.shape[0]-1) and y==(self.grid.shape[1] -1):
                    variation = 1000
                    # Check if mass has stabilised (TUNE THIS DEFINITION)
                    if self.time > 50:
                        variation = 0
                        stop = int(len(self.mass_history)*0.1)
                        for i in range(1,stop):
                            variation = abs(variation + self.mass_history[-i] / self.mass())
                        #     #print(f"variation {variation}")

                        # print(f"len {len(self.mass_history)}")
                        # print(f"stop {stop}")
                        # print(f"variation {variation}")
                        # print(f"time {self.time}")

                        if variation < 0.0:
                            return True

                        # if not stabilised,
                    self.drop_sand(n)

        self.avalanche(n)



    # You are free to define more methods within this class
