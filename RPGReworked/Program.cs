using System;
using System.Threading;

namespace RPGreworked
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.Clear();
            Options op = new Options();
            Story st = new Story();
            op.optionStart();
            st.Intro();

        }
    }
}
