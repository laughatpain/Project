import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class MinerNotFull
    extends Miner
{
    public MinerNotFull(String name, Point position, /*ArrayList imgs,*/ int animation_rate, int rate,
                        int resource_limit)
    {
        super(name, position, /*imgs,*/ animation_rate, rate, resource_limit);
    }
    public String entity_string ()
    {
        return ("miner" + name + position.xCoor() + position.yCoor() + resource_limit + rate
        + animation_rate);
    }
}
