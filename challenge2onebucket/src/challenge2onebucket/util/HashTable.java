package challenge2onebucket.util;

import java.util.*;


public class HashTable implements Map<String, String>
{
	
	
    private Entry[] mTable;
    private BoundedUniformHash mHash;
    
    public HashTable(final int n) {
        this.mTable = new Entry[n];
        (this.mHash = new ModLinearHash()).setBounds(n - 1);
    }
    
    private int getBucket(final Object o) {
      System.out.println("getbucket");
        this.mHash.reset();
        this.mHash.update((String)o);
        System.out.println("after getbucket");
        return (int)this.mHash.getHash();
    }
    
    private int getBucketAbs(final String o) {
      return 0;//(o.charAt(0) > 1) ? 0 : 1;
    }
    
     
    
    
    
    
    private Entry findEntry(final Object o, final boolean b) {
        return this.findEntry(o, this.getBucketAbs((String)o), b);
    }
    
    private Entry findEntryGet(final Object o, final boolean b) {
        return this.findEntryGet(o, this.getBucketAbs((String)o), b);
    }
    
    //counter for worst case complexity
    public int str_counter = 0;
    public int char_counter = 0;
   
    
     public boolean myEquals(char v1[], char v2[]) {
         int n = v1.length;
         if (n == v2.length) {
        	 int i = 0;
        	 while (n-- > 0) {	
         		 char_counter += 1; 
        		 if (v1[i] != v2[i]){
        			 return false;
        		 }
        		 i++;
        	 }
        	 return true;
         }
         return false;
     }	
    	
    
    //Interesting method for worst case complexity
    private Entry findEntry(final Object obj, final int n, final boolean b) {
      int i = 0;
      String strObj = (String)obj;
      char Obj1 [] = strObj.toCharArray();
      
        for (Entry next = this.mTable[n]; next != null; next = next.next) {
          System.out.println("before equals ");
          char Obj2 [] = next.key.toCharArray(); // get second array of chars
          if (next.key.equals(obj)){
        	  return next;
          }

            System.out.println("loop in findentry");
            i++;
        }
        System.out.println("after loop in findentry. iterated " + i);
        if (b) {
          System.out.println("Collision!");
            return this.mTable[n] = new Entry((String)obj, null, null, this.mTable[n]);
        }
        return null;
    }
    
    //Interesting method for worst case complexity
    private Entry findEntryGet(final Object obj, final int n, final boolean b) {
      int i = 0;
      String strObj = (String)obj;
      char Obj1 [] = strObj.toCharArray();
      
        for (Entry next = this.mTable[n]; next != null; next = next.next) {
          str_counter +=1;
          System.out.println("String counter " + str_counter);
          char Obj2 [] = next.key.toCharArray(); // get second array of chars
          if (myEquals(Obj1, Obj2)){
        	  return next;
          }
          System.out.println("Comparisons " + char_counter);
            System.out.println("loop in findentry");
            i++;
        }
        System.out.println("after loop in findentry. iterated " + i);
        if (b) {
          System.out.println("Collision!");
            return this.mTable[n] = new Entry((String)obj, null, null, this.mTable[n]);
        }
        return null;
    }
    
    public void clear() {
        for (int i = 0; i < this.mTable.length; ++i) {
            this.mTable[i] = null;
        }
    }
    
    public boolean containsKey(final Object o) {
        return this.findEntry(o, false) != null;
    }
    
    public boolean containsValue(final Object o) {
        for (int i = 0; i < this.mTable.length; ++i) {
            for (Entry next = this.mTable[i]; next != null; next = next.next) {
                if (next.value.equals(o)) {
                    return true;
                }
            }
        }
        return false;
    }
    
    public Set<Map.Entry<String, String>> entrySet() {
        return (Set<Map.Entry<String, String>>)new EntrySet();
    }
    
    public String get(final Object o) {
        final Entry entry = this.findEntryGet(o, false);
        if (entry == null) {
            return null;
        }
        return entry.value;
    }
    
    public boolean isEmpty() {
        for (int i = 0; i < this.mTable.length; ++i) {
            if (this.mTable[i] != null) {
                return false;
            }
        }
        return true;
    }
    
    public Set<String> keySet() {
        return (Set<String>)new KeySet();
    }
    
    public String put(final String s, final String value) {
        final Entry entry = this.findEntry(s, true);
        final String value2 = entry.value;
        entry.value = value;
        return value2;
    }
    
    public String putMask(final String s, final String value) {
        final Entry entry = this.findEntry(s, true);
        final String value2 = entry.value;
        entry.value = value;
        return value2;
    }
    
    public void putAll(final Map<? extends String, ? extends String> map) {
        for (final Map.Entry entry : map.entrySet()) {
            this.put((String)entry.getKey(), (String)entry.getValue());
        }
    }
    
    private void remove(final int n, final Entry entry) {
        if (entry.prev == null) {
            this.mTable[n] = entry.next;
        }
        else {
            entry.prev.next = entry.next;
        }
        if (entry.next != null) {
            entry.next.prev = entry.prev;
        }
    }
    
    public String remove(final Object o) {
        final int bucket = this.getBucket(o);
        final Entry entry = this.findEntry(o, bucket, false);
        if (entry == null) {
            return null;
        }
        this.remove(bucket, entry);
        return entry.value;
    }
    
    public int size() {
        int n = 0;
        for (int i = 0; i < this.mTable.length; ++i) {
            for (Entry next = this.mTable[i]; next != null; next = next.next) {
                ++n;
            }
        }
        return n;
    }
    
    public Collection<String> values() {
        return (Collection<String>)new ValuesCollection();
    }
    
    public String putIgnoreValue(final String s) {
        final Entry entry = this.findEntry(s, true);
        final String value2 = entry.value;
        entry.value = "value";
        return value2;
    }
    
    
    public class Entry implements Map.Entry<String, String>
    {
        String key;
        String value;
        Entry prev;
        Entry next;
        
        Entry(final String key, final String value, final Entry prev, final Entry next) {
            this.key = key;
            this.value = value;
            this.prev = prev;
            if (this.prev != null) {
                this.prev.next = this;
            }
            this.next = next;
            if (this.next != null) {
                this.next.prev = this;
            }
        }
        
        public boolean equals(final Object o) {
            if (o == null) {
                return false;
            }
            if (!(o instanceof Entry)) {
                return false;
            }
            final Entry entry = (Entry)o;
            if (this.key == null) {
                if (entry.key != null) {
                    return false;
                }
            }
            else if (!this.key.equals((Object)entry.key)) {
                return false;
            }
            if ((this.value != null) ? this.value.equals((Object)entry.value) : (entry.value == null)) {
                return true;
            }
            return false;
        }
        
        public String getKey() {
            return this.key;
        }
        
        public String getValue() {
            return this.value;
        }
        
        public int hashCode() {
            return ((this.key == null) ? 0 : this.key.hashCode()) ^ ((this.value == null) ? 0 : this.value.hashCode());
        }
        
        public String setValue(final String value) {
            final String value2 = this.value;
            this.value = value;
            return value2;
        }
    }
    
    private class EntryIterator implements Iterator<Map.Entry<String, String>>
    {
        private int mBucket;
        private Entry mEntry;
        
        EntryIterator() {
            this.mBucket = -1;
            this.mEntry = null;
        }
        
        public boolean hasNext() {
            if (this.mEntry != null && this.mEntry.next != null) {
                return true;
            }
            for (int i = this.mBucket + 1; i < HashTable.this.mTable.length; ++i) {
                if (HashTable.this.mTable[i] != null) {
                    return true;
                }
            }
            return false;
        }
        
        public Map.Entry<String, String> next() throws NoSuchElementException {
            if (this.mEntry != null && this.mEntry.next != null) {
                return (Map.Entry<String, String>)(this.mEntry = this.mEntry.next);
            }
            for (int i = this.mBucket + 1; i < HashTable.this.mTable.length; ++i) {
                if (HashTable.this.mTable[i] != null) {
                    this.mBucket = i;
                    return (Map.Entry<String, String>)(this.mEntry = HashTable.this.mTable[i]);
                }
            }
            throw new NoSuchElementException();
        }
        
        public void remove() {
            HashTable.this.remove(this.mBucket, this.mEntry);
        }
    }
    
    private class KeyIterator implements Iterator<String>
    {
        private EntryIterator mEntryIterator;
        
        KeyIterator() {
            this.mEntryIterator = new EntryIterator();
        }
        
        public boolean hasNext() {
            return this.mEntryIterator.hasNext();
        }
        
        public String next() throws NoSuchElementException {
            return (String)this.mEntryIterator.next().getKey();
        }
        
        public void remove() {
            this.mEntryIterator.remove();
        }
    }
    
    private class ValueIterator implements Iterator<String>
    {
        private EntryIterator mEntryIterator;
        
        ValueIterator() {
            this.mEntryIterator = new EntryIterator();
        }
        
        public boolean hasNext() {
            return this.mEntryIterator.hasNext();
        }
        
        public String next() throws NoSuchElementException {
            return (String)this.mEntryIterator.next().getValue();
        }
        
        public void remove() {
            this.mEntryIterator.remove();
        }
    }
    
    private class EntrySet implements Set<Map.Entry<String, String>>
    {
        public boolean add(final Map.Entry<String, String> entry) {
            throw new UnsupportedOperationException();
        }
        
        public boolean addAll(final Collection<? extends Map.Entry<String, String>> collection) {
            throw new UnsupportedOperationException();
        }
        
        public void clear() {
            HashTable.this.clear();
        }
        
        public boolean contains(final Object o) {
            final Map.Entry entry = (Map.Entry)o;
            return entry.equals((Object)HashTable.this.findEntry(entry.getKey(), false));
        }
        
        public boolean containsAll(final Collection<?> collection) {
            final Iterator iterator = collection.iterator();
            while (iterator.hasNext()) {
                if (!this.contains(iterator.next())) {
                    return false;
                }
            }
            return true;
        }
        
        public boolean isEmpty() {
            return HashTable.this.isEmpty();
        }
        
        public Iterator<Map.Entry<String, String>> iterator() {
            return (Iterator<Map.Entry<String, String>>)new EntryIterator();
        }
        
        public boolean remove(final Object o) {
            return HashTable.this.remove(((Map.Entry)o).getKey()) != null;
        }
        
        public boolean removeAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator iterator = collection.iterator();
            while (iterator.hasNext()) {
                if (this.remove(iterator.next())) {
                    b = true;
                }
            }
            return b;
        }
        
        public boolean retainAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator<Map.Entry<String, String>> iterator = this.iterator();
            try {
                while (true) {
                    if (!collection.contains(iterator.next())) {
                        iterator.remove();
                        b = true;
                    }
                }
            }
            catch (NoSuchElementException ex) {
                return b;
            }
        }
        
        public int size() {
            return HashTable.this.size();
        }
        
        public Object[] toArray() {
            final Object[] array = new Object[this.size()];
            int n = 0;
            final Iterator<Map.Entry<String, String>> iterator = this.iterator();
            while (iterator.hasNext()) {
                array[n] = iterator.next();
                ++n;
            }
            return array;
        }
        
        public <T> T[] toArray(T[] copy) {
            final int size = this.size();
            if (copy.length < size) {
                copy = (T[])Arrays.copyOf((Object[])copy, size);
            }
            else if (copy.length > size) {
                copy[size] = null;
            }
            int n = 0;
            final Iterator<Map.Entry<String, String>> iterator = this.iterator();
            while (iterator.hasNext()) {
                copy[n] = (T)iterator.next();
                ++n;
            }
            return copy;
        }
    }
    
    private class KeySet implements Set<String>
    {
        public boolean add(final String s) {
            throw new UnsupportedOperationException();
        }
        
        public boolean addAll(final Collection<? extends String> collection) {
            throw new UnsupportedOperationException();
        }
        
        public void clear() {
            HashTable.this.clear();
        }
        
        public boolean contains(final Object o) {
            return HashTable.this.containsKey(o);
        }
        
        public boolean containsAll(final Collection<?> collection) {
            final Iterator iterator = collection.iterator();
            while (iterator.hasNext()) {
                if (!this.contains(iterator.next())) {
                    return false;
                }
            }
            return true;
        }
        
        public boolean isEmpty() {
            return HashTable.this.isEmpty();
        }
        
        public Iterator<String> iterator() {
            return (Iterator<String>)new KeyIterator();
        }
        
        public boolean remove(final Object o) {
            return HashTable.this.remove(o) != null;
        }
        
        public boolean removeAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator iterator = collection.iterator();
            while (iterator.hasNext()) {
                if (this.remove(iterator.next())) {
                    b = true;
                }
            }
            return b;
        }
        
        public boolean retainAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator<String> iterator = this.iterator();
            try {
                while (true) {
                    if (!collection.contains(iterator.next())) {
                        iterator.remove();
                        b = true;
                    }
                }
            }
            catch (NoSuchElementException ex) {
                return b;
            }
        }
        
        public int size() {
            return HashTable.this.size();
        }
        
        public Object[] toArray() {
            final Object[] array = new Object[this.size()];
            int n = 0;
            final Iterator<String> iterator = this.iterator();
            while (iterator.hasNext()) {
                array[n] = iterator.next();
                ++n;
            }
            return array;
        }
        
        public <T> T[] toArray(T[] copy) {
            final int size = this.size();
            if (copy.length < size) {
                copy = (T[])Arrays.copyOf((Object[])copy, size);
            }
            else if (copy.length > size) {
                copy[size] = null;
            }
            int n = 0;
            final Iterator<String> iterator = this.iterator();
            while (iterator.hasNext()) {
                copy[n] = (T)iterator.next();
                ++n;
            }
            return copy;
        }
    }
    
    private class ValuesCollection implements Collection<String>
    {
        public boolean add(final String s) {
            throw new UnsupportedOperationException();
        }
        
        public boolean addAll(final Collection<? extends String> collection) {
            throw new UnsupportedOperationException();
        }
        
        public void clear() {
            HashTable.this.clear();
        }
        
        public boolean contains(final Object o) {
            return HashTable.this.containsValue(o);
        }
        
        public boolean containsAll(final Collection<?> collection) {
            final Iterator iterator = collection.iterator();
            while (iterator.hasNext()) {
                if (!this.contains(iterator.next())) {
                    return false;
                }
            }
            return true;
        }
        
        public boolean isEmpty() {
            return HashTable.this.isEmpty();
        }
        
        public Iterator<String> iterator() {
            return (Iterator<String>)new ValueIterator();
        }
        
        public boolean remove(final Object o) {
            final Iterator<String> iterator = this.iterator();
            try {
                while (!((String)iterator.next()).equals(o)) {}
                iterator.remove();
                return true;
            }
            catch (NoSuchElementException ex) {
                return false;
            }
        }
        
        public boolean removeAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator<String> iterator = this.iterator();
            try {
                while (true) {
                    if (collection.contains(iterator.next())) {
                        iterator.remove();
                        b = true;
                    }
                }
            }
            catch (NoSuchElementException ex) {
                return b;
            }
        }
        
        public boolean retainAll(final Collection<?> collection) {
            boolean b = false;
            final Iterator<String> iterator = this.iterator();
            try {
                while (true) {
                    if (!collection.contains(iterator.next())) {
                        iterator.remove();
                        b = true;
                    }
                }
            }
            catch (NoSuchElementException ex) {
                return b;
            }
        }
        
        public int size() {
            return HashTable.this.size();
        }
        
        public Object[] toArray() {
            final Object[] array = new Object[this.size()];
            int n = 0;
            final Iterator<String> iterator = this.iterator();
            while (iterator.hasNext()) {
                array[n] = iterator.next();
                ++n;
            }
            return array;
        }
        
        public <T> T[] toArray(T[] copy) {
            final int size = this.size();
            if (copy.length < size) {
                copy = (T[])Arrays.copyOf((Object[])copy, size);
            }
            else if (copy.length > size) {
                copy[size] = null;
            }
            int n = 0;
            final Iterator<String> iterator = this.iterator();
            while (iterator.hasNext()) {
                copy[n] = (T)iterator.next();
                ++n;
            }
            return copy;
        }
    }
}
