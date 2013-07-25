                // Delhi Metro Red Line
                
                var rlinepts = [
                        [28.72072, 77.10713],
                        [28.71483, 77.11467],
                        [28.7076, 77.12591], 
                        [28.70317, 77.13223],
                        [28.6981, 77.14024],
                        [28.69591, 77.15226], 
                        [28.68894, 77.1616],
                        [28.68254, 77.16459],
                        [28.67319, 77.16994],
                        [28.66999, 77.18169], 
                        [28.66662, 77.19882],
                        [28.66636, 77.20727],
                        [28.66711, 77.21653],
                        [28.6675, 77.22817],
                        [28.66800, 77.24994],
                        [28.66989, 77.26678],
                        [28.6718, 77.27756],
                        [28.67345, 77.28962],
                        [28.67544, 77.30095],
                        [28.67579, 77.31239],
                        [28.67592, 77.32142]
                ]
                
                for( i=0; i < rlinepts.length; i=i+1 ) {
                    rlinepts[ i ] = new L.LatLng( rlinepts[ i ][ 0 ], rlinepts[ i ][ 1 ] );
                }
                
                 line1 = new L.Polyline( rlinepts, { color: "red" } );
                 

                var redline = L.layerGroup([
                L.marker([28.72072, 77.10713],
                {icon: rmIcon}).bindPopup("<b>Rithala</b><br />Red Line<br />Elevated"),
                L.marker([28.71483, 77.11467],
                {icon: rmIcon}).bindPopup("<b>Rohini West</b><br />Red Line<br />Elevated"),
                L.marker([28.7076, 77.12591],
                {icon: rmIcon}).bindPopup("<b>Rohini East</b><br />Red Line<br />Elevated"),
                L.marker([28.70317, 77.13223],
                {icon: rmIcon}).bindPopup("<b>Pitam Pura</b><br/>Red Line<br />Elevated"),
                L.marker([28.6981, 77.14024],
                {icon: rmIcon}).bindPopup("<b>Kohat Enclave</b><br/>Red Line<br/>Elevated"),
                L.marker([28.69591, 77.15226],
                {icon: rmIcon}).bindPopup("<b>Netaji Subhash Place</b><br />Red Line<br />Elevated"),
                L.marker([28.68894, 77.1616],
                {icon: rmIcon}).bindPopup("<b>Keshav Puram</b><br />Red Line<br/>Elevated"),
                L.marker([28.68254, 77.16459],
                {icon: rmIcon}).bindPopup("<b>Kanhiya Nagar</b><br />Red Line<br />Elevated"),
                L.marker([28.67319, 77.16994],
                {icon: rmIcon}).bindPopup("<b>Inderlok</b><br />Red Line, Green Line<br />Elevated"),
                L.marker([28.66999, 77.18169],
                {icon: rmIcon}).bindPopup("<b>Shastri Nagar</b><br />Red Line<br />Elevated"),
                L.marker([28.66662, 77.19882],
                {icon: rmIcon}).bindPopup("<b>Pratap Nagar</b><br />Red Line<br />Elevated"),
                L.marker([28.66636, 77.20727],
                {icon: rmIcon}).bindPopup("<b>Pul Bangash</b><br />Red Line<br />Elevated"),
                L.marker([28.66711, 77.21653],
                {icon: rmIcon}).bindPopup("<b>Tis Hazari</b><br />Red Line<br />Elevated"),
                L.marker([28.6675, 77.22817],
                {icon: rmIcon}).bindPopup("<b>Kashmere Gate</b><br />Red Line, Yellow Line<br />Elevated(RL), Underground(YL)"),
                L.marker([28.668, 77.24994],
                {icon: rmIcon}).bindPopup("<b>Shastri Park</b><br />Red Line<br />At Grade"),
                L.marker([28.66989, 77.26678],
                {icon: rmIcon}).bindPopup("<b>Seelampur</b><br />Red Line<br />At Grade"),
                L.marker([28.6718, 77.27756],
                {icon: rmIcon}).bindPopup("<b>Welcome</b><br />Red Line<br />At Grade"),
                L.marker([28.67345, 77.28962],
                {icon: rmIcon}).bindPopup("<b>Shahdara</b><br />Red Line<br />At Grade"),
                L.marker([28.67544, 77.30095],
                {icon: rmIcon}).bindPopup("<b>Mansarovar Park</b><br />Red Line<br />Elevated"),
                L.marker([28.67579, 77.31239],
                {icon: rmIcon}).bindPopup("<b>Jhilmil</b><br />Red Line<br />Elevated"),
                L.marker([28.67592, 77.32142],
                {icon: rmIcon}).bindPopup("<b>Dilshad Garden</b><br />Red Line<br />Elevated"),
                line1]);
            
                
                
                // Delhi Metro Violet Line
                
                var vlinepts = [
                    [28.61474, 77.21191], 
                    [28.60276, 77.22829], 
                    [28.5904, 77.23326], 
                    [28.5843, 77.23766], 
                    [28.57079, 77.23653], 
                    [28.56417, 77.23423], 
                    [28.55527, 77.24205], 
                    [28.55148, 77.25154], 
                    [28.55007, 77.25835], 
                    [28.54451, 77.26401], 
                    [28.54292, 77.27504], 
                    [28.53824, 77.28319], 
                    [28.52878, 77.28826], 
                    [28.51938, 77.29388], 
                    [28.50254, 77.2993], 
                    [28.49334, 77.30307]
                  ]
               
                
                for( i=0; i < vlinepts.length; i=i+1 ) {
                    vlinepts[ i ] = new L.LatLng( vlinepts[ i ][ 0 ], vlinepts[ i ][ 1 ] );
                }
                
                 line2 = new L.Polyline( vlinepts, { color: "purple" } );
                 
                 
                var violetline = L.layerGroup([                 
                L.marker([28.61474, 77.21191],
                {icon: vmIcon}).bindPopup("<b>Central Secretariat</b><br />Yellow Line, Violet Line<br />Underground"),
                L.marker([28.60276, 77.22829],
                {icon: vmIcon}).bindPopup("<b>Khan Market</b><br />Violet Line<br />Underground"),
                L.marker([28.5904, 77.23326],
                {icon: vmIcon}).bindPopup("<b>Jawaharlal Nehru Stadium</b><br />Violet Line<br />Underground"),
                L.marker([28.5843, 77.23766],
                {icon: vmIcon}).bindPopup("<b>Jangpura</b><br />Violet Line<br />Underground"),
                L.marker([28.57079, 77.23653],
                {icon: vmIcon}).bindPopup("<b>Lajpat Nagar</b><br />Violet Line<br />Elevated"),
                L.marker([28.56417, 77.23423],
                {icon: vmIcon}).bindPopup("<b>Moolchand</b><br />Violet Line<br />Elevated"),
                L.marker([28.55527, 77.24205],
                {icon: vmIcon}).bindPopup("<b>Kailash Colony</b><br />Violet Line<br />Elevated"), 
                L.marker([28.55148, 77.25154],
                {icon: vmIcon}).bindPopup("<b>Nehru Place</b><br />Violet Line<br />Elevated"),
                L.marker([28.55007, 77.25835],
                {icon: vmIcon}).bindPopup("<b>Kalkaji Mandir</b><br />Violet Line<br />Elevated"),
                L.marker([28.54451, 77.26401],
                {icon: vmIcon}).bindPopup("<b>Govind Puri</b><br />Violet Line<br />Elevated"),
                L.marker([28.54292, 77.27504],
                {icon: vmIcon}).bindPopup("<b>Okhla</b><br />Violet Line<br />Elevated"),
                L.marker([28.53824, 77.28319],
                {icon: vmIcon}).bindPopup("<b>Jasola Apollo</b><br />Violet Line<br />Elevated"),
                L.marker([28.52878, 77.28826],
                {icon: vmIcon}).bindPopup("<b>Sarita Vihar</b><br />Violet Line<br />Elevated"),
                L.marker([28.51938, 77.29388],
                {icon: vmIcon}).bindPopup("<b>Mohan Estate</b><br />Violet Line<br />Elevated"),
                L.marker([28.50254, 77.2993],
                {icon: vmIcon}).bindPopup("<b>Tughlakabad</b><br />Violet Line<br />Elevated"),
                L.marker([28.49334, 77.30307],
                {icon: vmIcon}).bindPopup("<b>Badarpur</b><br />Violet Line<br />Elevated"),
                line2]);
                
                
                var blinepts = [
                    [28.57466, 77.35608], 
					[28.56714, 77.34598], 
					[28.56409, 77.3342], 
					[28.57081, 77.32612], 
					[28.57819, 77.31757], 
					[28.58512, 77.31139], 
					[28.58916, 77.30204], 
					[28.59428, 77.29455], 
					[28.60442, 77.28925], 
					[28.61806, 77.27869], 
					[28.62331, 77.26792], 
					[28.62051, 77.24993], 
					[28.62342, 77.2425], 
					[28.62588, 77.2341], 
					[28.63003, 77.22436], 
					[28.63282, 77.21826], 
					[28.63923, 77.2084], 
					[28.64427, 77.19988], 
					[28.644, 77.18855], 
					[28.6425, 77.17815], 
					[28.64498, 77.16929], 
					[28.6516, 77.15824], 
					[28.65655, 77.1514], 
					[28.65784, 77.14248], 
					[28.65274, 77.13164], 
					[28.64902, 77.1227], 
					[28.64379, 77.11284], 
					[28.64039, 77.10495], 
					[28.63657, 77.09648], 
					[28.63305, 77.08669], 
					[28.62943, 77.07767], 
					[28.62481, 77.0653], 
					[28.62177, 77.05585], 
					[28.62025, 77.04514], 
					[28.61932, 77.03326], 
					[28.61564, 77.02197], 
					[28.60223, 77.02588], 
					[28.59722, 77.03326], 
					[28.59232, 77.04051], 
					[28.58657, 77.04929], 
					[28.58068, 77.05682], 
					[28.57487, 77.06454], 
					[28.56583, 77.06706], 
					[28.55226, 77.05828]
			    ]
			    
			    for( i=0; i < blinepts.length; i=i+1 ) {
                    blinepts[ i ] = new L.LatLng( blinepts[ i ][ 0 ], blinepts[ i ][ 1 ] );
                }    
                
                line7 = new L.Polyline( blinepts, { color: "blue" } );
                
                var blinebpts = [
                    [28.64997, 77.33974], 
					[28.64544, 77.32432], 
					[28.64695, 77.31603], 
					[28.64849, 77.30558], 
					[28.64171, 77.29543], 
					[28.63663, 77.28683], 
					[28.63064, 77.27749], 
					[28.62331, 77.26792]
			    ]
			    
			     for( i=0; i < blinebpts.length; i=i+1 ) {
                    blinebpts[ i ] = new L.LatLng( blinebpts[ i ][ 0 ], blinebpts[ i ][ 1 ] );
                }    
                
                line8 = new L.Polyline( blinebpts, { color: "blue" } );
               
                
                var blueline  = L.layerGroup([                 
                L.marker([28.57466, 77.35608],
                {icon: bmIcon}).bindPopup("<b>Noida City Centre</b><br />Blue Line<br />Elevated"),
                L.marker([28.56714, 77.34598],
                {icon: bmIcon}).bindPopup("<b>Noida Golf Course</b><br />Blue Line<br />Elevated"),
                L.marker([28.56409, 77.3342],
                {icon: bmIcon}).bindPopup("<b>Botanical Garden</b><br />Blue Line<br />Elevated"),
                L.marker([28.57081, 77.32612],
                {icon: bmIcon}).bindPopup("<b>Noida Sector 18</b><br />Blue Line<br />Elevated"),
                L.marker([28.57819, 77.31757],
                {icon: bmIcon}).bindPopup("<b>Noida Sector 16</b><br />Blue Line<br />Elevated"),
                L.marker([28.58512, 77.31139],
                {icon: bmIcon}).bindPopup("<b>Noida Sector 15</b><br />Blue Line<br />Elevated"),
                L.marker([28.58916, 77.30204],
                {icon: bmIcon}).bindPopup("<b>New Ashok Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.59428, 77.29455],
                {icon: bmIcon}).bindPopup("<b>Mayur Vihar Extension</b><br />Blue Line<br />Elevated"),
                L.marker([28.60442, 77.28925],
                {icon: bmIcon}).bindPopup("<b>Mayur Vihar -I</b><br />Blue Line<br />Elevated"),
                L.marker([28.61806, 77.27869],
                {icon: bmIcon}).bindPopup("<b>Akshardham</b><br />Blue Line<br />Elevated"),
                L.marker([28.62331, 77.26792],
                {icon: bmIcon}).bindPopup("<b>Yamuna Bank</b><br />Blue Line<br />At-Grade"),
                L.marker([28.62051, 77.24993],
                {icon: bmIcon}).bindPopup("<b>Indraprastha</b><br />Blue Line<br />Elevated"),
                L.marker([28.62342, 77.2425],
                {icon: bmIcon}).bindPopup("<b>Pragati Maidan</b><br />Blue Line<br />Elevated"),
                L.marker([28.62588, 77.2341],
                {icon: bmIcon}).bindPopup("<b>Mandi House</b><br />Blue Line<br />Underground"),
                L.marker([28.63003, 77.22436],
                {icon: bmIcon}).bindPopup("<b>Barakhambha Road</b><br />Blue Line<br />Underground"),
                L.marker([28.63282, 77.21826],
                {icon: bmIcon}).bindPopup("<b>Rajiv Chowk</b><br />Yellow Line, Blue Line<br />Underground"),
                L.marker([28.63923, 77.2084],
                {icon: bmIcon}).bindPopup("<b>Ramakrishna Ashram Marg</b><br />Blue Line<br />Elevated"),
                L.marker([28.64427, 77.19988],
                {icon: bmIcon}).bindPopup("<b>Jhandewalan</b><br />Blue Line<br />Elevated"),
                L.marker([28.644, 77.18855],
                {icon: bmIcon}).bindPopup("<b>Karol Bagh</b><br />Blue Line<br />Elevated"),
                L.marker([28.6425, 77.17815],
                {icon: bmIcon}).bindPopup("<b>Rajendra Place</b><br />Blue Line<br />Elevated"),
                L.marker([28.64498, 77.16929],
                {icon: bmIcon}).bindPopup("<b>Patel Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.6516, 77.15824],
                {icon: bmIcon}).bindPopup("<b>Shadipur</b><br />Blue Line<br />Elevated"),
                L.marker([28.65655, 77.1514],
                {icon: bmIcon}).bindPopup("<b>Kirti Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.65784, 77.14248],
                {icon: bmIcon}).bindPopup("<b>Moti Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.65274, 77.13164],
                {icon: bmIcon}).bindPopup("<b>Ramesh Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.64902, 77.1227],
                {icon: bmIcon}).bindPopup("<b>Rajouri Garden</b><br />Blue Line<br />Elevated"),
                L.marker([28.64379, 77.11284],
                {icon: bmIcon}).bindPopup("<b>Tagore Garden</b><br />Blue Line<br />Elevated"),
                L.marker([28.64039, 77.10495],
                {icon: bmIcon}).bindPopup("<b>Subhash Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.63657, 77.09648],
                {icon: bmIcon}).bindPopup("<b>Tilak Nagar</b><br />Blue Line<br />Elevated"),
                L.marker([28.63305, 77.08669],
                {icon: bmIcon}).bindPopup("<b>Janakpuri East</b><br />Blue Line<br />Elevated"),
                L.marker([28.62943, 77.07767],
                {icon: bmIcon}).bindPopup("<b>Janakpuri West</b><br />Blue Line<br />Elevated"),
                L.marker([28.62481, 77.0653],
                {icon: bmIcon}).bindPopup("<b>Uttam Nagar East</b><br />Blue Line<br />Elevated"),
                L.marker([28.62177, 77.05585],
                {icon: bmIcon}).bindPopup("<b>Uttam Nagar West</b><br />Blue Line<br />Elevated"),
                L.marker([28.62025, 77.04514],
                {icon: bmIcon}).bindPopup("<b>Nawada</b><br />Blue Line<br />Elevated"),
                L.marker([28.61932, 77.03326],
                {icon: bmIcon}).bindPopup("<b>Dwarka Morh</b><br />Blue Line<br />Elevated"),
                L.marker([28.61564, 77.02197],
                {icon: bmIcon}).bindPopup("<b>Dwarka</b><br />Blue Line<br />Elevated"),
                L.marker([28.60223, 77.02588],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 14</b><br />Blue Line<br />Elevated"),
                L.marker([28.59722, 77.03326],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 13</b><br />Blue Line<br />Elevated"),
                L.marker([28.59232, 77.04051],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 12</b><br />Blue Line<br />Elevated"),
                L.marker([28.58657, 77.04929],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 11</b><br />Blue Line<br />Elevated"),
                L.marker([28.58068, 77.05682],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 10</b><br />Blue Line<br />Elevated"),
                L.marker([28.57487, 77.06454],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 9</b><br />Blue Line<br />Elevated"),
                L.marker([28.56583, 77.06706],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 8</b><br />Blue Line<br />Elevated"),
                L.marker([28.55226, 77.05828],
                {icon: bmIcon}).bindPopup("<b>Dwarka Sector 21</b><br />Blue Line<br />Underground"),
                L.marker([28.64997, 77.33974],
                {icon: bmIcon}).bindPopup("<b>Vaishali</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.64544, 77.32432],
                {icon: bmIcon}).bindPopup("<b>Kaushambi</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.64695, 77.31603],
                {icon: bmIcon}).bindPopup("<b>Anand Vihar</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.64849, 77.30558],
                {icon: bmIcon}).bindPopup("<b>Karkarduma</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.64171, 77.29543],
                {icon: bmIcon}).bindPopup("<b>Preet Vihar</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.63663, 77.28683],
                {icon: bmIcon}).bindPopup("<b>Nirman Vihar</b><br />Blue Line branch<br />Elevated"),
                L.marker([28.63064, 77.27749],
                {icon: bmIcon}).bindPopup("<b>Laxmi Nagar</b><br />Blue Line branch<br />Elevated"),line7,line8]);
                
                
                // Delhi Metro Yellow Line
                
                var ylinepts = [
                    [28.72592, 77.16267], 
                    [28.71642, 77.17046], 
                    [28.70696, 77.18053], 
                    [28.70278, 77.19363], 
                    [28.69785, 77.20722], 
                    [28.6948, 77.21483], 
                    [28.68802, 77.2214], 
                    [28.67726, 77.2241], 
                    [28.6675, 77.22817], 
                    [28.65785, 77.23014], 
                    [28.64931, 77.22637], 
                    [28.64307, 77.22144], 
                    [28.63282, 77.21826], 
                    [28.62295, 77.21389], 
                    [28.61474, 77.21191], 
                    [28.61166, 77.21198], 
                    [28.59726, 77.21088], 
                    [28.58708, 77.21209], 
                    [28.57526, 77.20935], 
                    [28.56892, 77.20771], 
                    [28.55979, 77.20682], 
                    [28.54335, 77.20667], 
                    [28.52798, 77.20565], 
                    [28.5206, 77.20138], 
                    [28.51302, 77.18648], 
                    [28.50671, 77.17484], 
                    [28.49927, 77.16153], 
                    [28.49383, 77.14922], 
                    [28.48076, 77.12583], 
                    [28.48203, 77.10232], 
                    [28.48182, 77.09235], 
                    [28.47957, 77.08006], 
                    [28.47209, 77.07175], 
                    [28.45927, 77.07268]
                ]
                
                for( i=0; i < ylinepts.length; i=i+1 ) {
                    ylinepts[ i ] = new L.LatLng( ylinepts[ i ][ 0 ], ylinepts[ i ][ 1 ] );
                }
                
                 line3 = new L.Polyline( ylinepts, { color: "yellow" } );

                var yellowline = L.layerGroup([ 
                L.marker([28.72592, 77.16267],
				{icon: ymIcon}).bindPopup("<b>Jahangirpuri</b><br />Yellow Line<br />Underground"),
                L.marker([28.71642, 77.17046],
				{icon: ymIcon}).bindPopup("<b>Adarsh Nagar</b><br />Yellow Line<br />Underground"),
                L.marker([28.70696, 77.18053],
				{icon: ymIcon}).bindPopup("<b>Azadpur</b><br />Yellow Line<br />Underground"),
                L.marker([28.70278, 77.19363],
				{icon: ymIcon}).bindPopup("<b>Model Town</b><br />Yellow Line<br />Underground"),
                L.marker([28.69785, 77.20722],
				{icon: ymIcon}).bindPopup("<b>GTB Nagar</b><br />Yellow Line<br />Underground"),
                L.marker([28.6948, 77.21483],
				{icon: ymIcon}).bindPopup("<b>Vishwa Vidyalaya</b><br />Yellow Line<br />Underground"),
                L.marker([28.68802, 77.2214],
				{icon: ymIcon}).bindPopup("<b>Vidhan Sabha</b><br />Yellow Line<br />Underground"),
                L.marker([28.67726, 77.2241],
				{icon: ymIcon}).bindPopup("<b>Civil Lines</b><br />Yellow Line<br />Underground"),
                L.marker([28.6675, 77.22817],
				{icon: ymIcon}).bindPopup("<b>Kashmere Gate</b><br />Red Line, Yellow Line<br />Elevated(RL), Underground(YL)"),
                L.marker([28.65785, 77.23014],
				{icon: ymIcon}).bindPopup("<b>Chandni Chowk</b><br />Yellow Line<br />Underground"),
                L.marker([28.64931, 77.22637],
				{icon: ymIcon}).bindPopup("<b>Chawri Bazar</b><br />Yellow Line<br />Underground"),
                L.marker([28.64307, 77.22144],
				{icon: ymIcon}).bindPopup("<b>New Delhi</b><br />Yellow Line, Airport Express<br />Underground"),
                L.marker([28.63282, 77.21826],
				{icon: ymIcon}).bindPopup("<b>Rajiv Chowk</b><br />Yellow Line, Blue Line<br />Underground"),
                L.marker([28.62295, 77.21389],
				{icon: ymIcon}).bindPopup("<b>Patel Chowk</b><br />Yellow Line<br />Underground"),
                L.marker([28.61474, 77.21191],
				{icon: ymIcon}).bindPopup("<b>Central Secretariat</b><br />Yellow Line, Violet Line<br />Underground"),
                L.marker([28.61166, 77.21198],
				{icon: ymIcon}).bindPopup("<b>Udyog Bhawan</b><br />Yellow Line<br />Underground"),
                L.marker([28.59726, 77.21088],
				{icon: ymIcon}).bindPopup("<b>Race Course</b><br />Yellow Line<br />Underground"),
                L.marker([28.58708, 77.21209],
				{icon: ymIcon}).bindPopup("<b>Jor Bagh</b><br />Yellow Line<br />Underground"),
                L.marker([28.57526, 77.20935],
				{icon: ymIcon}).bindPopup("<b>INA</b><br />Yellow Line<br />Underground"),
                L.marker([28.56892, 77.20771],
				{icon: ymIcon}).bindPopup("<b>AIIMS</b><br />Yellow Line<br />Underground"),
                L.marker([28.55979, 77.20682],
				{icon: ymIcon}).bindPopup("<b>Green Park</b><br />Yellow Line<br />Underground"),
                L.marker([28.54335, 77.20667],
				{icon: ymIcon}).bindPopup("<b>Hauz Khas</b><br />Yellow Line<br />Underground"),
                L.marker([28.52798, 77.20565],
				{icon: ymIcon}).bindPopup("<b>Malviya Nagar</b><br />Yellow Line<br />Underground"),
                L.marker([28.5206, 77.20138],
				{icon: ymIcon}).bindPopup("<b>Saket</b><br />Yellow Line<br />Underground"),
                L.marker([28.51302, 77.18648],
				{icon: ymIcon}).bindPopup("<b>Qutab Minar</b><br />Yellow Line<br />Elevated"),
                L.marker([28.50671, 77.17484],
				{icon: ymIcon}).bindPopup("<b>Chhatarpur</b><br />Yellow Line<br />Elevated"),
                L.marker([28.49927, 77.16153],
				{icon: ymIcon}).bindPopup("<b>Sultanpur</b><br />Yellow Line<br />Elevated"),
                L.marker([28.49383, 77.14922],
				{icon: ymIcon}).bindPopup("<b>Ghitorni</b><br />Yellow Line<br />Elevated"),
                L.marker([28.48076, 77.12583],
				{icon: ymIcon}).bindPopup("<b>Arjan Garh</b><br />Yellow Line<br />Elevated"),
                L.marker([28.48203, 77.10232],
				{icon: ymIcon}).bindPopup("<b>Guru Dronacharya</b><br />Yellow Line<br />Elevated"),
                L.marker([28.48182, 77.09235],
				{icon: ymIcon}).bindPopup("<b>Sikandarpur</b><br />Yellow Line<br />Elevated"),
                L.marker([28.47957, 77.08006],
				{icon: ymIcon}).bindPopup("<b>MG Road</b><br />Yellow Line<br />Elevated"),
                L.marker([28.47209, 77.07175],
				{icon: ymIcon}).bindPopup("<b>IFFCO Chowk</b><br />Yellow Line<br />Elevated"),
                L.marker([28.45927, 77.07268],
				{icon: ymIcon}).bindPopup("<b>HUDA City Centre</b><br />Yellow Line<br />Elevated"),
                line3]);
                
                // Delhi Metro Green Line
                
                var glinepts = [
                    [28.67319, 77.16994], 
					[28.67153, 77.15527], 
					[28.67289, 77.14614], 
					[28.6749, 77.13056], 
					[28.67734, 77.11965], 
					[28.6773, 77.11228], 
					[28.67855, 77.10227], 
					[28.67959, 77.09261], 
					[28.6809, 77.08077], 
					[28.6818, 77.07385], 
					[28.68231, 77.06471], 
					[28.68208, 77.05596], 
					[28.68221, 77.04381], 
					[28.68321, 77.03133]
				]
                 
                for( i=0; i < glinepts.length; i=i+1 ) {
                    glinepts[ i ] = new L.LatLng( glinepts[ i ][ 0 ], glinepts[ i ][ 1 ] );
                }    
                
                line5 = new L.Polyline( glinepts, { color: "green" } );
                
                var glblinepts = [
                    [28.67153, 77.15527],
					[28.66199, 77.15748],  
					[28.65575, 77.15057]
				] 
                
                for( i=0; i < glblinepts.length; i=i+1 ) {
                    glblinepts[ i ] = new L.LatLng( glblinepts[ i ][ 0 ], glblinepts[ i ][ 1 ] );
                }    
                
                line6 = new L.Polyline( glblinepts, { color: "green" } );
                
                var greenline = L.layerGroup([ 
                L.marker([28.67319, 77.16994],
                {icon: gmIcon}).bindPopup("<b>Inderlok</b><br />Red Line, Green Line<br />Elevated"),
                L.marker([28.67153, 77.15527],
                {icon: gmIcon}).bindPopup("<b>Ashok Park Main</b><br />Green Line<br />Elevated"),
                L.marker([28.67289, 77.14614],
                {icon: gmIcon}).bindPopup("<b>Punjabi Bagh East</b><br />Green Line<br />Elevated"),
                L.marker([28.6749, 77.13056],
                {icon: gmIcon}).bindPopup("<b>Shivaji Park</b><br />Green Line<br />Elevated"),
                L.marker([28.67734, 77.11965],
                {icon: gmIcon}).bindPopup("<b>Madipur</b><br />Green Line<br />Elevated"),
                L.marker([28.6773, 77.11228],
                {icon: gmIcon}).bindPopup("<b>Paschim Vihar East</b><br />Green Line<br />Elevated"),
                L.marker([28.67855, 77.10227],
                {icon: gmIcon}).bindPopup("<b>Paschim Vihar West</b><br />Green Line<br />Elevated"),
                L.marker([28.67959, 77.09261],
                {icon: gmIcon}).bindPopup("<b>Peera Garhi</b><br />Green Line<br />Elevated"),
                L.marker([28.6809, 77.08077],
                {icon: gmIcon}).bindPopup("<b>Udyog Nagar</b><br />Green Line<br />Elevated"),
                L.marker([28.6818, 77.07385],
                {icon: gmIcon}).bindPopup("<b>Surajmal Stadium</b><br />Green Line<br />Elevated"),
                L.marker([28.68231, 77.06471],
                {icon: gmIcon}).bindPopup("<b>Nangloi</b><br />Green Line<br />Elevated"),
                L.marker([28.68208, 77.05596],
                {icon: gmIcon}).bindPopup("<b>Nangloi Railway station</b><br />Green Line<br />Elevated"),
                L.marker([28.68221, 77.04381],
                {icon: gmIcon}).bindPopup("<b>Rajdhani Park</b><br />Green Line<br />Elevated"),
                L.marker([28.68321, 77.03133],
                {icon: gmIcon}).bindPopup("<b>Mundka</b><br />Green Line<br />Elevated"),
                L.marker([28.66199, 77.15748],
                {icon: gmIcon}).bindPopup("<b>Satguru Ramsingh Marg</b><br />Green Line<br />Elevated"),
                L.marker([28.65575, 77.15057],
                {icon: gmIcon}).bindPopup("<b>Kirti Nagar</b><br />Blue Line, Green Line<br />Elevated"),
                line5,line6]);
                
                
                
                // Delhi Metro Airport Express
       
                var aelinepts = [
                    [28.64307, 77.22144], 
				    [28.62901, 77.2119], 
				    [28.59178, 77.16155], 
				    [28.54881, 77.12092], 
				    [28.55693, 77.08669], 
				    [28.55226, 77.05828]
				]
				
				for( i=0; i < aelinepts.length; i=i+1 ) {
                    aelinepts[ i ] = new L.LatLng( aelinepts[ i ][ 0 ], aelinepts[ i ][ 1 ] );
                }
                
                 line4 = new L.Polyline( aelinepts, { color: "orange" } );
                 
                var airport = L.layerGroup([
                L.marker([28.64307, 77.22144],
                {icon: omIcon}).bindPopup("<b>New Delhi</b><br />Yellow Line, Airport Express<br />Underground"), L.marker([28.62901, 77.2119],
                {icon: omIcon}).bindPopup("<b>Shivaji Stadium</b><br />Airport Express<br />Underground"),
                L.marker([28.59178, 77.16155],
                {icon: omIcon}).bindPopup("<b>Dhaula Kuan</b><br />Airport Express<br />Elevated"),
                L.marker([28.54881, 77.12092],
                {icon: omIcon}).bindPopup("<b>Delhi Aerocity</b><br />Airport Express<br />Underground"),
                L.marker([28.55693, 77.08669],
                {icon: omIcon}).bindPopup("<b>Indira Gandhi International Airport</b><br />Airport Express<br />Underground"),
                L.marker([28.55226, 77.05828],
                {icon: omIcon}).bindPopup("<b>Dwarka Sector 21</b><br />Blue Line, Airport Express<br />Underground"),line4]);

    
                var map = L.map('map',{
                    center: new L.LatLng(28.635, 77.224), 
                    zoom: 11,
                    layers:[ cloudmadelayer ]
                    });
                
                var baseMaps = {
                    "Google Map": googlelayer,
			        "Cloudmade Map": cloudmadelayer,
			        "Bing" : BingAerialWithLabels
		        };
		        
		        var overlayMaps = {
		            "Red Line Metro" : redline,
		            "Violet Line Metro" :violetline,
		            "Blue Line Metro" : blueline,
		            "Yellow Line Metro" : yellowline,
		            "Green Line Metro" : greenline,
			        "Airport Express Metro": airport
		        };

                 L.control.layers(baseMaps,overlayMaps).addTo(map);
