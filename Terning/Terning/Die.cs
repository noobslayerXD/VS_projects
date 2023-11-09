using System;
using System.Collections.Generic;
using System.Text;

namespace Terning
{
    class Die
    {
        public int noOfEyes;
        Random rand = new Random();

        public void roll()
        {
            noOfEyes = rand.Next(1, 7);
        }
        public void getEyes()
        {
            Console.WriteLine(noOfEyes);
        }
    }
}
