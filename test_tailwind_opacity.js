const themeColor = (varName) => {
    return ({ opacityValue }) => {
        if (opacityValue !== undefined) {
            return `color-mix(in srgb, var(${varName}) ${opacityValue * 100}%, transparent)`;
        }
        return `var(${varName})`;
    };
};

console.log(themeColor('--theme-bg')({ opacityValue: 0.5 }));
console.log(themeColor('--theme-bg')({}));
