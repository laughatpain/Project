import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class Ore
    extends NotAnimated
{
    public Ore (String name, Point position, /*ArrayList imgs,*/ int rate)
    {
        super (name, /*imgs,*/ position, rate = 5000);
    }
    public String entity_string ()
    {
        return ("ore" + name + position.xCoor() + position.yCoor() + rate);
    }
}
