import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class OreBlob
    extends MovingRate
{
    public OreBlob (String name, Point position, /*ArrayList imgs,*/ int rate, int animation_rate)
    {
        super (name, position, /*imgs,*/ rate, animation_rate);
    }
    public String entity_string()
    {
        return ("obstacle" + name + position.xCoor() + position.yCoor());
    }
}
