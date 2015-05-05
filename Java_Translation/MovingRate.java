import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class MovingRate
    extends Moving
{
    protected int rate;

    public MovingRate (String name, Point position, /*ArrayList imgs,*/ int animation_rate, int rate)
    {
        super (name, position, /*imgs,*/ animation_rate);
        this.rate = rate;
    }
    public int get_rate ()
    {
        return rate;
    }
}
