public class Simulator {

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
