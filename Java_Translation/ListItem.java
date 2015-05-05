/**
 * Created by James on 5/4/2015.
 */
public class ListItem
{
    protected Object item;
    protected int ord;

    public ListItem (Object item, int ord)
    {
        this.item = item;
        this.ord = ord;
    }
    public boolean equals(Object o)
    {
        if (!(o instanceof ListItem))return false;
        ListItem b = (ListItem) o;
        return item == b.item && ord == b.ord;
    }
}
