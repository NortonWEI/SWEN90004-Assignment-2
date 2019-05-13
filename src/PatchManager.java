import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.function.Predicate;
import java.util.stream.Collectors;

/**
 * Manager class for Patch objects
 */
class PatchManager implements Tickable {
    /**
     * All patches stored
     */
    private Patch[] patches;

    /**
     * Construct a new Patch manager.
     */
    PatchManager() {
        patches = new Patch[Params.NUM_PATCH()];

        // Initialise all patches
        int patchIndex = 0;
        for (int i = 0; i < Params.MAP_WIDTH; i++) {
            for (int j = 0; j < Params.MAP_HEIGHT; j++) {
                patches[patchIndex] = new Patch(i, j);
                patchIndex ++;
            }
        }
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void update() {
        // Dont need to do anything
    }

    /**
     * Get all neighbour patches of a patch.
     * @param patch the patch to be searched
     * @return list of neighbour patches
     */
    private ArrayList<Patch> getNeighbours(Patch patch) {
        ArrayList<Patch> neighbours = new ArrayList<>();

        for (Patch currPatch: patches) {
            if (currPatch == patch) {
                continue;
            }

            if (currPatch.isNeighbour(patch)) {
                neighbours.add(currPatch);
            }
        }

        return neighbours;
    }

    /**
     * Get an random, unoccupied patch.
     * @return a patch
     */
    Patch getRandomUnoccupiedPatch() {
        Patch patch;

        do {
            Random r = new Random();
            int index = r.nextInt(patches.length + 1);
            patch = patches[index];
        } while (!patch.isOccupied());

        return patch;
    }

    /**
     * Get the filtered list of neighbour turtle based on the filter function
     * @param patch the patch to be searched around
     * @param filterFunction the filter function to be applied for
     * @return the list of turtles
     */
    ArrayList<Turtle> filterNeighbourTurtle(Patch patch, Predicate<Turtle> filterFunction) {
        ArrayList<Patch> neighbourPatches = getNeighbours(patch);
        final ArrayList<Turtle> neighbourTurtles = new ArrayList<>();

        // For each neighbour patch, find all matching turtles and add to the final list
        neighbourPatches.forEach((p) -> {
            List<Turtle> turtles = p.getTurtles()
                    .stream()
                    .filter(filterFunction)
                    .collect(Collectors.toList());

            neighbourTurtles.addAll(turtles);
        });

        return neighbourTurtles;
    }

    /**
     * Count the number of turtle objects satisfying the required turtle class and the (optional) filter function.
     * @param patch the patch to be searched into
     * @param turtleClass the turtle class to be compared with
     * @param filterFunction the filter function to be applied for, set null if not applicable
     * @return the number of turtle objects
     */
    int getNeighbourTurtleCount(Patch patch, Class turtleClass, Predicate<Turtle> filterFunction) {
        ArrayList<Turtle> neighbours = filterNeighbourTurtle(patch, (turtle ->
            turtleClass.isInstance(turtle) && (filterFunction == null || filterFunction.test(turtle))
        ));

        return neighbours.size();
    }
}
