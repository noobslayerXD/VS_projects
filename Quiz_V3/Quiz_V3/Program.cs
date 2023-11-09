using System;

namespace Quiz_V3
{
    class Program
    {
        static void Main(string[] args)
        {
            int guess;
            bool guesstext;
            Console.WriteLine("Hvad er 6+9");
            guess = Convert.ToInt32(Console.ReadLine());
            int point = 0;
            if (guess == 6 + 9)
            {
                point++;
                Console.WriteLine($"Det var rigtigt!! Du får et point, du har nu {point} point");
                Console.WriteLine("Hvad er 4*2");
                guess = Convert.ToInt32(Console.ReadLine());
                if (guess == 4 * 2)
                {
                    point++;
                    Console.WriteLine("Det var rigtigt!! Du får et point, du har nu " + point + " point");
                    Console.WriteLine("Har du en allergi? True or false");
                    guesstext = Convert.ToBoolean(Console.ReadLine());
                    if (guesstext == false)
                    {
                        point++;
                        Console.WriteLine("Godt, du får et point. Du har " + point + " point");
                        while (point > 0) 
                        {
                            Random Rand = new Random();
                            int num1 = Rand.Next(1, 100);
                            int num2 = Rand.Next(1, 100);
                            int num3 = Rand.Next(1, 4);
                            switch (num3)
                            {
                                case 1:
                                    Console.WriteLine($"{num1} + {num2}");
                                    guess = Convert.ToInt32(Console.ReadLine());
                                    if (guess == num1 + num2)
                                    {
                                        point++;
                                        Console.WriteLine($"Det var rigtigt!! Du får et point, du har nu {point} point");
                                    }
                                    else
                                    {
                                        point--;
                                        Console.WriteLine($"Det var forkert!!Det rigtige svar var {num1 + num2} Du har nu {point} point");
                                    }
                                    break;
                                case 2:
                                    Console.WriteLine($"{num1} - {num2}");
                                    guess = Convert.ToInt32(Console.ReadLine());
                                    if (guess == num1 - num2)
                                    {
                                        point++;
                                        Console.WriteLine($"Det var rigtigt!! Du får et point, du har nu {point} point");
                                    }
                                    else
                                    {
                                        point--;
                                        Console.WriteLine($"Det var forkert!!Det rigtige svar var {num1 - num2} Du har nu {point} point");
                                    }
                                    break;
                                case 3:
                                    Console.WriteLine($"{num1} * {num2}");
                                    guess = Convert.ToInt32(Console.ReadLine());
                                    if (guess == num1 * num2)
                                    {
                                        point++;
                                        Console.WriteLine($"Det var rigtigt!! Du får et point, du har nu {point} point");
                                    }
                                    else
                                    {
                                        point--;
                                        Console.WriteLine($"Det var forkert!!Det rigtige svar var {num1 * num2} Du har nu {point} point");
                                    }
                                    break;
                                case 4:
                                    Console.WriteLine($"{num1} / {num2}");
                                    guess = Convert.ToInt32(Console.ReadLine());
                                    if (guess == num1 / num2)
                                    {
                                        point++;
                                        Console.WriteLine($"Det var rigtigt!! Du får et point, du har nu {point} point");
                                    }
                                    else
                                    {
                                        point--;
                                        Console.WriteLine($"Det var forkert!!Det rigtige svar var {num1 / num2} Du har nu {point} point");
                                    }
                                    break;
                            }
                        }
                    }
                    else
                    {
                        point--;
                        Console.WriteLine($"Svagt. Du har nu {point} point");
                    }
                }
                else
                {
                    Console.WriteLine($"Du svarede forkert, du fik {point} point");
                }
            }
            else
            {
                Console.WriteLine($"Du svarede forkert, du fik {point} point");
            }
        }
    }
}