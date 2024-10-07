// SPDX-License-Identifier: MIT
pragma solidity ^0.8.21;

import {Utils} from './Utils.sol';
import {Random, RandomCtx} from './Random.sol';

/**
 * @author Eto Vass
 */

contract BasicSVGRenderer2 {
    function renderSVG(uint tokenId) public pure returns (string memory) {
        RandomCtx memory ctx = Random.initCtx(tokenId);

        string memory circles = "";

        // Flashing effect by creating different hues and opacity patterns
        for (uint i=0; i < 100; i++) { 
            int cx = Random.randRange(ctx, 0, 512);
            int cy = Random.randRange(ctx, 0, 512);
            int r = Random.randRange(ctx, 20, 100); // Larger range for more size variance
            int hue = Random.randRange(ctx, 0, 359); // Random hue per circle
            int sat = Random.randRange(ctx, 70, 100); // High saturation for vivid colors
            int lightness = Random.randRange(ctx, 50, 80); // Lightness for brightness effect
            int opacity = Random.randRange(ctx, 50, 99); // Higher opacity for stronger flashes

            // Create concentric circles or flashing layers
            circles = string.concat(circles, 
                '<circle cx="', Utils.toString(cx), 
                '" cy="', Utils.toString(cy), 
                '" r="', Utils.toString(r),
                '" fill="hsl(', Utils.toString(hue), ',', Utils.toString(sat), 
                '%, ', Utils.toString(lightness), '%)" opacity="0.', Utils.toString(opacity), '"/>');
        }

        return string.concat('<svg xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMinYMin meet" viewBox="0 0 512 512">',circles,'</svg>');
    }
}