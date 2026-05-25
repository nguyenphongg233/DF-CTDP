#include<bits/stdc++.h> 

using namespace std;

void run(string test_name, int num_nodes, int num_districts){
    string cmd = "python3 PlanarGraphGenerator.py no-visualize " + to_string(num_nodes) + " " + to_string(num_districts) + " 0.05 > " + test_name + ".dat";
    system(cmd.c_str());
    // cerr << "Generated test case: " << test_name << ".dat" << endl;
    // cerr << cmd << "\n";
}
void generate_affinity(string test_name, string output_name, int num_nodes, int num_districts, string type = "H"){
    string cmd = "python3 AffinityGenerator.py " + test_name + ".dat " + output_name + " " + type;
    system(cmd.c_str());
    // cerr << "Generated affinity for test case: " << test_name << ".dat" << endl;
    cerr << cmd << "\n";
    //python3 AffinityGenerator.py Non_affinity_instances/DU50-5-0.dat H-Non_affinity_instances/DU50-5-0-affinity.dat H
}
signed main(){
    vector<pair<string,pair<int,int>>> test_cases = {
        {"DU50-5",{50,5}}
        // {"DU500-20", {500, 20}},
        // {"DU500-50", {500, 50}},
        // {"DU1000-20", {1000, 20}},
        // {"DU1000-50", {1000, 50}},
    };

    system("mkdir -p Non_affinity_instances");
    system("mkdir -p Affinity_instances");
    for(int i = 0; i < (int)test_cases.size(); i++){
        string test_name = test_cases[i].first;
        int num_nodes = test_cases[i].second.first;
        int num_districts = test_cases[i].second.second;

        for(int j = 0;j < 5;j++){
            run("Non_affinity_instances/" + test_name + "-" + to_string(j), num_nodes, num_districts);
            generate_affinity("Non_affinity_instances/" + test_name + "-" + to_string(j), "Affinity_instances/H_" + test_name + "-" + to_string(j) + ".dat", num_nodes, num_districts, "H");
            generate_affinity("Non_affinity_instances/" + test_name + "-" + to_string(j), "Affinity_instances/I1_" + test_name + "-" + to_string(j) + ".dat", num_nodes, num_districts, "I1");
            generate_affinity("Non_affinity_instances/" + test_name + "-" + to_string(j), "Affinity_instances/I2_" + test_name + "-" + to_string(j) + ".dat", num_nodes, num_districts, "I2");
        }
    }
}