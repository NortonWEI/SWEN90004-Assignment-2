import java.util.ArrayList;
import java.util.Random;

/**
 * Simulates a Cop.
 */
class Cop extends Turtle {
    /**
     * Construct a new Cop object.
     * @param world the world this cop is in
     */
    Cop(World world) {
        super(world);
    }

    /**
     * {@inheritDoc}
     */
    @Override
    public void update() {
        super.update();
        enforce();
    }

    /**
     * Find and arrest a random active agent in the neighbourhood
     */
    private void enforce() {
        // Find all active agents in the neighbourhood
        ArrayList<Turtle> agents = world.getPatchManager().filterNeighbourTurtle(patch, (turtle ->
            turtle instanceof Agent && ((Agent) turtle).isActive()
        ));

        // Select a random one from the matched agents
        Random r = new Random();
        int index = r.nextInt(agents.size() + 1);
        Agent suspect = (Agent) agents.get(index);

        // Move to the patch of the (about-to-be) jailed agent
        moveToPatch(suspect.getPatch());

        // Arrest suspect
        suspect.setActive(false);
        suspect.setJailTerm(r.nextInt(Params.MAX_JAILED_TERM + 1));
    }
}
