import numpy as np
import scipy as sp

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


        self.mass_history = np.append(self.mass_history, n)
        self.time += 1


        print(f"grid before: {self.grid}")


    def mass(self):
        """Return the mass of the grid."""

        return np.sum(self.grid)

    def topple(self, site):
        """Topple the specified site."""
        self.grid[site] -= 4
        x = site[0]
        y = site[1]

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

        elif x==(self.width - 1):
            self.grid[x+1][y] += 1
            self.grid[x][y+1] += 1
            self.grid[x][y-1] += 1


    def avalanche(self):
        """Run the avalanche causing all sites to topple and store the stats of
        the avalanche in the appropriate variables.

        """

        max_topple = 5
        event = 0
        self.drop_sand(100)


        for x in range(self.grid.shape[0]):
            for y in range(self.grid.shape[1]):

                if self.grid[x,y] >= 4:
                    self.topple((x,y))
                    event += 1

                if event == max_topple:
                    break

        

    # You are free to define more methods within this class
