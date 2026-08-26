const withOpacity = (varName) => {
    return ({ opacityValue }) => {
        if (opacityValue !== undefined) {
            return `color-mix(in srgb, var(${varName}) calc(${opacityValue} * 100%), transparent)`;
        }
        return `var(${varName})`;
    };
};

console.log(withOpacity('--theme-bg')({ opacityValue: 'var(--tw-bg-opacity)' }));
console.log(withOpacity('--theme-bg')({ opacityValue: 0.5 }));
console.log(withOpacity('--theme-bg')({}));
