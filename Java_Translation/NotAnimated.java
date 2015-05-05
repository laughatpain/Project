import java.util.ArrayList;

/**
 * Created by James on 5/3/2015.
 */
public class NotAnimated
    extends Entity
{
    protected int rate;
    public NotAnimated (String name, /*ArrayList imgs,*/ Point position, int rate)
    {
        super (name, /*imgs,*/ position);
        this.rate = rate;
    }
    public int get_rate ()
    {
        return rate;
    }
}
