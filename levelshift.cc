/*
 * Input format:  timestamp value
 * Output format: timestamp value rsi
 * Options:
 *	-B <binsize>
 *	-L <cutoff> (number of (possibly binned) entries used for calculation)
 *	-T <t_value>
 *	-H <Huberweight>
 *	-t transform input values by taking log10 of them.
 */
#include <iostream>
#include <fstream>
#include <iomanip> // setprecision()
#include <vector>
#include <cmath> // abs(), log10()
#include <algorithm> // min(), sort()
#include <numeric> // accumulate()
#include <unistd.h> // getopt()
#include <map>

using namespace std;

inline double mean(const vector<double>& data)
{
    return accumulate(data.begin(), data.end(), 0.0) / data.size();
}
 
inline double variance(const vector<double>& data)
{
    double my_mean = mean(data);
    double temp = 0.0;
    for (int i = 0; i < data.size(); i++) {
	 temp += (data[i] - my_mean) * (data[i] - my_mean) ;
    }
    return temp / (data.size()-1);
}

double cusum(const vector<double>& input, int index, double up_down, double dev, double huberweight, int l, bool goesup)
{
    // How many items are in our time series following the passed index
    int rem = input.size() - index;
    int length = min(l, rem);
    double sum_weights = 0;
    double norm_cumsum = 0;
    for (int i=index; i<(index+length); i++) {
        // normalized deviation of our variable outside the range mean+thresh 
        double my_norm_dev = (input[i]-up_down)/sqrt(dev);
        // Huber's weight values to de-emphasize large deviations 
        double arg_w_two = huberweight/abs(my_norm_dev);
        double my_weight = min(1.0, arg_w_two);
        // Sum Huber weight to normalize the cumsum with later 
        sum_weights += my_weight;
	// Integrate weighted deviations -- If the integral is always
	// positive, it confirms the presence of a consistent upward shift
        norm_cumsum += my_norm_dev*my_weight;
	// No regime change if the normalized cumulative sum turns to be
	// negative at any point {2:L} (or positive when sum going down)
        if ((goesup && norm_cumsum < 0) || (!goesup && norm_cumsum > 0)) {
            return 0;
        }
    }
    if(sum_weights > 0) {
        norm_cumsum = norm_cumsum/sum_weights;
    }
    return norm_cumsum;
}

double rsi(const vector<double>& input, int index, double up, double low, double dev, double huberweight, int l)
{
    double r = 0;
    if (input[index] > up) {
	// Upward shift
        r = cusum(input,index,up,dev,huberweight,l,true);
    } else if (input[index] < low) {
	// Downward shift
	r = cusum(input,index,low,dev,huberweight,l,false);
    }    
    return r;
}

/*
 * Calculation of the mean estimate for a given range using Huber's weights
 * The Huber's function is defined as min( 1, * param/(|res|/scale))
 * param: a given parameter (huberweight); affects the range where weights = 1
 * res: deviation from the mean estimate (I used the median as the first
 * approximation)
 * scale: estimate of variation. Some use 1.483*(median absolute deviation,
 * or MAD, of the deviations of the data from their median). I used std,
 * i.e. dev
 * See http://www.stat.berkeley.edu/~stark/Preprints/Oersted/writeup.htm
 * The procedure consists of two iterations. At the first iteration the
 * estimate of the regime average is the simple unweighed arithmetic mean.
 * In the second iteration it is weighed average from the first iteration.
*/

double getweightedaverage(const vector<double>& input, double dev)
{
    double mean_r1 = mean(input);

    for (int k=0; k<2; k++)
    {
        double sum_weights = 0;
        double sum_mean = 0;
        for (int i=0; i<input.size(); i++)
        {
            double my_norm_dev = (input[i]-mean_r1)/sqrt(dev);
            double arg_w_two = 10000000;
            if (abs(my_norm_dev)>0) {
              arg_w_two = 1/abs(my_norm_dev);
            }
            double my_weight = min(1.0, arg_w_two);
            sum_weights += my_weight;
            sum_mean += my_weight * my_norm_dev;
        }
        sum_mean = sum_mean/sum_weights;
        sum_mean = sum_mean*sqrt(dev) + mean_r1;
        mean_r1 = sum_mean;
    }
    return mean_r1;
}

int main(int argc, char ** argv)
{
    int binsize = 0;
    bool transform = false;
    //to get the t_value, use the student's t-test table for 2n-2
    //degrees of freedom, where n is the cutoff. select a confidence
    //level and two-tailed test
    //the t_value below is for cutoff=10 and 99% confidence level with
    //the two-tailed test
    double t_value = 2.878;
    double huberweight = 1.0;
    int cutoff = 10;
    char opt;
    while ((opt = getopt(argc, argv, "B:L:T:H:t")) != -1) {
        switch (opt) {
            case 'B':
		binsize = atoi(optarg);
                break;
            case 'L':
		cutoff = atoi(optarg);
                break;
            case 'T':
		t_value = strtod(optarg, NULL);
                break;
            case 'H':
		huberweight = strtod(optarg, NULL);
                break;
            case 't':
		transform = true;
                break;
            default:
                cerr << "Unknown option given: " << opt << endl;
                exit(1);
        }
    }

    vector<int> tstamps;
    vector<double> values;
    int timestamp = 0;
    double in_val = 0.0;
    map<int, double> binned;
    while (cin >> timestamp >> in_val) {
	if (in_val == 0.0) {
	    continue;
	}
	if (transform) {
	    in_val = log10(in_val);
	}
	int binned_stamp = timestamp;
	if (binsize > 0) {
	    binned_stamp = (timestamp / binsize) * binsize;
	}
	map<int, double>::iterator existing = binned.find(binned_stamp);
	if (existing == binned.end() || in_val < existing->second) {
	    binned[binned_stamp] = in_val;
	}
    }
    for(map<int, double>::iterator it = binned.begin(); it != binned.end();
	    it++)
    {
	tstamps.push_back(it->first);
	values.push_back(it->second);
    }

    vector<double> var_all;
    for (int i=0; i<cutoff; i++) {
    }
    for (int i=cutoff; i<values.size(); i++) {
	vector<double> tmp;
	for (int j=0; j<cutoff; j++) {
	    tmp.push_back(values[i-cutoff+j]);
	}
	var_all.push_back(variance(tmp));
    }
    double mean_var = mean(var_all);
    double diff = t_value * (sqrt(2*mean_var/cutoff));

    // initial regime the first l values
    vector<double> tmp;
    for (int i=0; i<cutoff; i++) {
	tmp.push_back(values[i]);
    }

    double mean_r1 = getweightedaverage(tmp, mean_var);
    double upper = mean_r1 + diff;
    double lower = mean_r1 - diff;
    int cp = 0;
    double rsi_val;
    for (int i=1; i < values.size(); i++) {
	// Get the corresponding regime shift index 
	rsi_val = rsi(values, i, upper, lower, mean_var, huberweight, cutoff);
	// Terminate if there is a a regime shift with no enough points to
	// characterize it!
	if (abs(rsi_val)>0 && i > values.size()-cutoff) {
	    break;
	}
	if (rsi_val != 0) {
	    cout << tstamps[i] << "\t" << values[i] << "\t"
		<< setprecision(13) << rsi_val << endl;
	}
	vector<double> tmp2;
	if (rsi_val == 0) {
	    if (cp+cutoff <= i) {
		for (int j=cp; j<=i; j++) {
		    tmp2.push_back(values[j]);
		}
		mean_r1 = getweightedaverage(tmp2, mean_var);
		upper = mean_r1+diff;
		lower = mean_r1-diff;
	    }
	} else {
	    cp = i;
	    for (int j=i; j<=(i+cutoff-1); j++) {
		tmp2.push_back(values[j]);
	    }
	    mean_r1 = getweightedaverage(tmp2, mean_var);
	    upper = mean_r1+diff;
	    lower = mean_r1-diff;
	}
    }
    return 0;
}
