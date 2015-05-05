import java.util.ArrayList;
import java.util.List;

/**
 * Created by James on 5/3/2015.
 */
public class OrderedList
{
    protected ArrayList<ListItem> list;

    public OrderedList ()
    {
       this.list = new ArrayList<ListItem>();
    }
    public void insert (Object item, int ord)
    {

        int size = list.size();
        int idx = 0;
        while (idx < size && list.get(idx).ord < ord)
        {
            idx += 1;
        }
        list.add(idx, new ListItem(item,ord));
        //list [idx:idx] = [ListItem (item,ord)];
    }
    public void remove (Object item)
    {
        int size = list.size();
        int idx = 0;
        while (idx < size && !list.get(idx).equals(item))
        {
            idx += 1;
        }
        if (idx < size)
        {
           list.remove(idx);
        }
    }
    public ListItem head ()
    {
        return list.get(0);

    }
    public ListItem pop ()
    {
        return list.remove(0);
    }

}
