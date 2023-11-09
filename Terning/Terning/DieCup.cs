using System;
using System.Collections.Generic;
using System.Text;

namespace Terning
{
    class DieCup
    {
        Random rand = new Random();
        int Die1;
        int Die2;
        public void roll()
        {
            Die1 = rand.Next(1, 7);
            Die2 = rand.Next(1, 7);
        }
        public void getEyes()
        {
            int PenisCup = Die1 + Die2;
            Console.WriteLine(PenisCup);
        }
    }
}
