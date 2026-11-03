#include <math.h>

// Knightly Deviation
float kdev(float * data, int n)
{
    float sum = 0;

    for (int i = 0; i < n - 1; i += 1)
    {
        float dist = sqrt(pow(data[i] - data[i+1], 2));
        sum += dist;
    }

    float mean = sum / n;
    
    return sqrt(mean);
}