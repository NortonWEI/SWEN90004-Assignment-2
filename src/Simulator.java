/**
 * The main class for simulation.
 *
 * @author Dafu Ai, Wenzhou Wei
 */
public class Simulator {

    /**
     * Runs the simulation
     */
    public static void main(String[] args) throws InterruptedException {
        int tick = 0;
        World world = new World();

        while (true) {
            System.out.println("Frame #" + tick);
            world.update();
            System.out.println("");

            Thread.sleep(1000);
            tick ++;
        }
    }
}
