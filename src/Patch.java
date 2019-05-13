import java.util.ArrayList;
import java.util.function.Function;
import java.util.function.Predicate;

/**
 * Simulates a Patch
 */
public class Patch {
    /**
     * All turtles in the patch.
     */
    private ArrayList<Turtle> turtles;

    /**
     * x coordinate of this patch.
     */
    private int x;

    /**
     * y coordinate of this patch.
     */
    private int y;

    /**
     * Initialise a new Patch object.
     * @param x x coordinate
     * @param y y coordinate
     */
    Patch(int x, int y) {
        this.x = x;
        this.y = y;
        this.turtles = new ArrayList<>();
    }

    /**
     * Get the x coordinate of the patch.
     * @return x coordinate
     */
    public int getX() {
        return x;
    }

    /**
     * Get the y coordinate of the patch.
     * @return y coordinate
     */
    public int getY() {
        return y;
    }

    /**
     * Add a turtle.
     * @param turtle the turtle to be added
     */
    void addTurtle(Turtle turtle) {
        turtles.add(turtle);
    }

    /**
     * Remove a turtle.
     * @param turtle the turtle to be removed
     */
    public void removeTurtle(Turtle turtle) {
        turtles.remove(turtle);
    }

    /**
     * Checks and return whether this patch is occupied.
     * @return true if occupied; false otherwise
     */
    boolean isOccupied() {
        for (Turtle turtle: turtles) {
            if (turtle instanceof Cop) {
                return true;
            }

            if (turtle instanceof Agent && !((Agent) turtle).isJailed()) {
                return true;
            }
        }

        return false;
    }

    /**
     * Determine whether the specified patch is a neighbour to this patch.
     * @param patch the patch to be compared
     * @return true if it's neighbour; false otherwise.
     */
    boolean isNeighbour(Patch patch) {
        double distance = Math.sqrt(Math.pow((patch.getX()-x), 2) + Math.pow((patch.getY()-y),2));
        return distance <= Params.VISION;
    }

    /**
     * Get all turtles.
     * @return list of turtles
     */
    public ArrayList<Turtle> getTurtles() {
        return turtles;
    }
}
