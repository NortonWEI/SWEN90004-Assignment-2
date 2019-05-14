import java.util.ArrayList;
import java.util.Collections;

/**
 * Simulates a world of agents, cops and patches.
 *
 * @author Dafu Ai
 */
class World implements Tickable {
    /**
     * All patches.
     */
    private PatchMap patchMap;

    /**
     * All turtles.
     */
    private ArrayList<Turtle> turtles;

    /**
     * Construct a new World object.
     */
    World() {
        patchMap = new PatchMap();
        turtles = new ArrayList<>();

        for (int i=0; i<Params.NUM_COP(); i++) {
            turtles.add(new Cop(this));
        }

        for (int i=0; i<Params.NUM_AGENT(); i++) {
            turtles.add(new Agent(this));
        }
    }

    /**
     * Get the patch map.
     * @return the patch map
     */
    PatchMap getPatchMap() {
        return patchMap;
    }

    /**
     * Update the world.
     */
    @Override
    public void update() {
        patchMap.update();

        // Shuffle all turtles so they perform action in a random sequence
        Collections.shuffle(turtles);
        turtles.forEach(Turtle::update);
    }
}
