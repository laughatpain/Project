import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Miner
    extends MovingRate
{
    protected int resource_limit;
    protected int resource_count;

    public Miner (String name, Point position, /*ArrayList imgs,*/ int animation_rate, int rate,
                  int resource_limit)
    {
        super (name, position, /*imgs,*/ animation_rate, rate);
        this.resource_limit = resource_limit;
        this.resource_count = 0;
    }
    public void set_resource_count (int n)
    {
        resource_count = n;
    }
    public int get_resource_count ()
    {
        return resource_count;
    }
    public int get_resource_limit()
    {
        return resource_limit;
    }
}
