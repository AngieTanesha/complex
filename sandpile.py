import numpy as np
import scipy as sp
import seaborn as sns


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


        # ONLY STEP 1
        while np.amax(self.grid) < 4:

            self.drop_sand(n)
            self.time += 1

            np.append(self.mass_history, self.mass())

        # STEP 2 and 3 there are toppling
        while np.amax(self.grid) > 3:


            # get critical points
            x, y = np.where(self.grid > 3)

            # topple critical points
            for i in range(len(x)):
                site = (x[i], y[i])

                self.topple(site)
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

        # STEP 4 TOPPLING DONE
        return True





    # You are free to define more methods within this class
